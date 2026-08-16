"""
Student Mental Health Database Service Module
=============================================
จัดการตรรกะการเพิ่ม การดึงข้อมูล และการนำเข้าไฟล์ CSV ลงตาราง mental_health_records ใน MySQL Database
รองรับทั้ง User Defined Column Mapping และ Dynamic Column Mapping
"""

import io
import os
import pandas as pd
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from app.models.db_models import MentalHealthRecord
from app.models.schemas import MentalHealthCreate, ImportCSVResponse, CSVColumnMapping, EducationLevel

# ตารางชื่อเรียกคอลัมน์พัวพันหลายรูปแบบ (Column Aliases Mapping)
COLUMN_ALIASES = {
    "time_date": ["timestamp", "time_date", "time", "date", "created_at"],
    "gender": ["choose your gender", "gender", "sex"],
    "age": ["age", "student_age"],
    "education_level": [
        "education level",
        "education_level",
        "education",
        "education_level_code",
        "level of education",
        "study level",
        "degree level",
        "ระดับการศึกษา"
    ],
    "course": ["what is your course?", "course", "major", "department", "degree"],
    "year_of_study": ["your current year of study", "year_of_study", "year of study", "year"],
    "cgpa": ["what is your cgpa?", "cgpa", "gpa"],
    "marital_status": ["marital status", "marital_status"],
    "depression": ["do you have depression?", "depression"],
    "anxiety": ["do you have anxiety?", "anxiety"],
    "panic_attack": ["do you have panic attack?", "panic_attack", "panic attack"],
    "specialist_treatment": [
        "did you seek any specialist for a treatment?",
        "specialist_treatment",
        "specialist treatment",
        "treatment"
    ]
}

# ตารางแปลงชื่อระดับการศึกษาแบบเต็ม / ตัวย่อ ให้เป็น Enum รหัสมาตรฐาน
EDUCATION_LEVEL_MAP = {
    # PP: Pre-primary Education (การศึกษาก่อนประถมศึกษา)
    "pp": "PP",
    "pre_primary": "PP",
    "pre-primary": "PP",
    "pre-primary education": "PP",
    "pre primary education": "PP",
    "อนุบาล": "PP",
    "ก่อนประถมศึกษา": "PP",

    # PE: Primary Education (ประถมศึกษา)
    "pe": "PE",
    "primary_education": "PE",
    "primary": "PE",
    "primary education": "PE",
    "ประถม": "PE",
    "ประถมศึกษา": "PE",

    # LSE: Lower Secondary Education (มัธยมศึกษาตอนต้น)
    "lse": "LSE",
    "lower_secondary_education": "LSE",
    "lower secondary": "LSE",
    "lower secondary education": "LSE",
    "มัธยมศึกษาตอนต้น": "LSE",
    "ม.ต้น": "LSE",

    # USE_VS: Upper Secondary Education / Vocational Stream (มัธยมศึกษาตอนปลาย / สายอาชีวศึกษา)
    "use_vs": "USE_VS",
    "upper secondary education / vocational stream": "USE_VS",
    "upper secondary education": "USE_VS",
    "upper secondary": "USE_VS",
    "vocational stream": "USE_VS",
    "vocational": "USE_VS",
    "มัธยมศึกษาตอนปลาย": "USE_VS",
    "ม.ปลาย": "USE_VS",
    "ปวช": "USE_VS",
    "ปวช.": "USE_VS",

    # BBDL: Below bachelor's degree level (ต่ำกว่าปริญญาตรี / อนุปริญญา / ปวส.)
    "bbdl": "BBDL",
    "below bachelor's degree level": "BBDL",
    "below bachelor": "BBDL",
    "diploma": "BBDL",
    "อนุปริญญา": "BBDL",
    "ปวส": "BBDL",
    "ปวส.": "BBDL",

    # BD: Bachelor's degree (ปริญญาตรี)
    "bd": "BD",
    "bachelor's degree": "BD",
    "bachelor": "BD",
    "bachelor degree": "BD",
    "undergraduate": "BD",
    "ปริญญาตรี": "BD",
    "ป.ตรี": "BD",

    # MD: Master's Degree (ปริญญาโท)
    "md": "MD",
    "master's degree": "MD",
    "master": "MD",
    "master degree": "MD",
    "postgraduate": "MD",
    "ปริญญาโท": "MD",
    "ป.โท": "MD",

    # PHD: Doctoral Degree (ปริญญาเอก)
    "phd": "PHD",
    "doctoral degree": "PHD",
    "doctorate": "PHD",
    "doctoral": "PHD",
    "ปริญญาเอก": "PHD",
    "ป.เอก": "PHD",

    # UNK: Unknown / Not Specified (ไม่ระบุ / ไม่ทราบข้อมูล)
    "unk": "UNK",
    "unknown": "UNK",
    "none": "UNK",
    "n/a": "UNK",
    "-": "UNK",
    "": "UNK"
}


def normalize_education_level(val: Optional[Union[str, EducationLevel]]) -> str:
    """
    แปลงค่าระดับการศึกษาให้อยู่ในรูปแบบ Enum Code (PP, PE, LSE, USE_VS, BBDL, BD, MD, PHD, UNK)
    หากไม่ระบุหรือค่าว่าง จะได้ผลลัพธ์เป็น 'UNK' อัตโนมัติ
    """
    if not val:
        return "UNK"
    if isinstance(val, EducationLevel):
        return val.value
    clean_val = str(val).strip().lower()
    return EDUCATION_LEVEL_MAP.get(clean_val, "UNK")


def extract_value_by_alias(
    row: pd.Series,
    field_key: str,
    user_mapped_col: Optional[str] = None,
    default: Optional[str] = None
) -> Optional[str]:
    """
    ดึงค่าจากแถว CSV โดยลองตรวจหาจาก user_mapped_col ก่อน หากไม่มีให้ตรวจจาก Aliases
    """
    # 1. ลองดึงจากชื่อ Column ที่ User ระบุมาใน Mapping Body ก่อน
    if user_mapped_col and user_mapped_col in row.index:
        val = row[user_mapped_col]
        if pd.notnull(val):
            return str(val).strip()

    # 2. หากหาตาม User Mapping ไม่เจอ ให้ตรวจจาก Aliases อัตโนมัติ (Case-Insensitive Match)
    aliases = [user_mapped_col] if user_mapped_col else []
    aliases.extend(COLUMN_ALIASES.get(field_key, []))

    for col in row.index:
        col_clean = str(col).strip().lower()
        for alias in aliases:
            if alias and col_clean == str(alias).strip().lower():
                val = row[col]
                if pd.notnull(val):
                    return str(val).strip()

    return default


def create_mental_health_record(db: Session, record: MentalHealthCreate) -> MentalHealthRecord:
    """
    บันทึกข้อมูลสุขภาพจิตนักเรียน 1 รายการลง MySQL Database
    """
    db_record = MentalHealthRecord(
        time_date=record.time_date,
        gender=record.gender,
        age=record.age,
        education_level=normalize_education_level(record.education_level),
        course=record.course,
        year_of_study=record.year_of_study,
        cgpa=record.cgpa,
        marital_status=record.marital_status,
        depression=record.depression,
        anxiety=record.anxiety,
        panic_attack=record.panic_attack,
        specialist_treatment=record.specialist_treatment
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_mental_health_records(db: Session, skip: int = 0, limit: int = 100) -> List[MentalHealthRecord]:
    """
    ดึงรายการข้อมูลสุขภาพจิตนักเรียนจาก MySQL Database (เรียงลำดับ ID ล่าสุดก่อน)
    """
    return db.query(MentalHealthRecord).order_by(MentalHealthRecord.id.desc()).offset(skip).limit(limit).all()


def get_student_statistics(db: Session) -> dict:
    """
    คำนวณสถิติภาพรวมข้อมูลสุขภาพจิตนักเรียนในฐานข้อมูล
    """
    total = db.query(MentalHealthRecord).count()
    if total == 0:
        return {
            "total_count": 0,
            "depression_count": 0,
            "anxiety_count": 0,
            "panic_count": 0,
            "treatment_count": 0,
            "high_risk_count": 0,
            "low_risk_count": 0
        }

    dep_count = db.query(MentalHealthRecord).filter(MentalHealthRecord.depression.ilike("yes")).count()
    anx_count = db.query(MentalHealthRecord).filter(MentalHealthRecord.anxiety.ilike("yes")).count()
    panic_count = db.query(MentalHealthRecord).filter(MentalHealthRecord.panic_attack.ilike("yes")).count()
    treat_count = db.query(MentalHealthRecord).filter(MentalHealthRecord.specialist_treatment.ilike("yes")).count()

    # High risk cases (any condition is Yes)
    high_risk_count = db.query(MentalHealthRecord).filter(
        (MentalHealthRecord.depression.ilike("yes")) |
        (MentalHealthRecord.anxiety.ilike("yes")) |
        (MentalHealthRecord.panic_attack.ilike("yes"))
    ).count()

    return {
        "total_count": total,
        "depression_count": dep_count,
        "anxiety_count": anx_count,
        "panic_count": panic_count,
        "treatment_count": treat_count,
        "high_risk_count": high_risk_count,
        "low_risk_count": max(0, total - high_risk_count)
    }


def delete_mental_health_record(db: Session, record_id: int) -> bool:
    """
    ลบรายการข้อมูลนักเรียนตาม ID
    """
    rec = db.query(MentalHealthRecord).filter(MentalHealthRecord.id == record_id).first()
    if rec:
        db.delete(rec)
        db.commit()
        return True
    return False


def clear_all_mental_health_records(db: Session) -> int:
    """
    ล้างข้อมูลทั้งหมดในตาราง mental_health_records
    """
    count = db.query(MentalHealthRecord).delete()
    db.commit()
    return count


def make_record_signature(
    time_date: Optional[str],
    gender: Optional[str],
    age: Optional[Union[int, str]],
    education_level: Optional[Union[str, EducationLevel]],
    course: Optional[str],
    year_of_study: Optional[str],
    cgpa: Optional[str],
    marital_status: Optional[str],
    depression: Optional[str],
    anxiety: Optional[str],
    panic_attack: Optional[str],
    specialist_treatment: Optional[str]
) -> tuple:
    """
    สร้าง Unique Signature สำหรับเปรียบเทียบข้อมูลแถวว่าเหมือนกันทุกประการหรือไม่
    (ตัดช่องว่างส่วนเกินและแปลงเป็นตัวพิมพ์เล็กเพื่อความแม่นยำในการเปรียบเทียบ)
    """
    try:
        age_int = int(age) if age is not None and str(age).strip() != "" else 0
    except (ValueError, TypeError):
        age_int = 0

    return (
        str(time_date or "").strip(),
        str(gender or "").strip().lower(),
        age_int,
        normalize_education_level(education_level).lower(),
        str(course or "").strip().lower(),
        str(year_of_study or "").strip().lower(),
        str(cgpa or "").strip().lower(),
        str(marital_status or "").strip().lower(),
        str(depression or "").strip().lower(),
        str(anxiety or "").strip().lower(),
        str(panic_attack or "").strip().lower(),
        str(specialist_treatment or "").strip().lower()
    )


def process_df_to_db(
    db: Session,
    df: pd.DataFrame,
    mapping: Optional[CSVColumnMapping] = None
) -> ImportCSVResponse:
    """
    แปลงข้อมูลจาก Pandas DataFrame ลงตาราง mental_health_records
    โดยตรวจเช็คว่าถ้าข้อมูลใน DB กับในไฟล์เหมือนกันอยู่แล้ว จะไม่ insert ซ้ำ แต่ถ้าต่างกัน/เป็นข้อมูลใหม่ จะเพิ่มลง DB
    """
    # ดึง Signature ของข้อมูลที่มีอยู่แล้วในฐานข้อมูลเพื่อป้องกันข้อมูลซ้ำซ้อน
    existing_rows = db.query(
        MentalHealthRecord.time_date,
        MentalHealthRecord.gender,
        MentalHealthRecord.age,
        MentalHealthRecord.education_level,
        MentalHealthRecord.course,
        MentalHealthRecord.year_of_study,
        MentalHealthRecord.cgpa,
        MentalHealthRecord.marital_status,
        MentalHealthRecord.depression,
        MentalHealthRecord.anxiety,
        MentalHealthRecord.panic_attack,
        MentalHealthRecord.specialist_treatment
    ).all()

    existing_signatures = {
        make_record_signature(
            r.time_date, r.gender, r.age, r.education_level, r.course, r.year_of_study,
            r.cgpa, r.marital_status, r.depression, r.anxiety,
            r.panic_attack, r.specialist_treatment
        )
        for r in existing_rows
    }

    imported_count = 0
    skipped_count = 0

    m_time = mapping.time_date if mapping else None
    m_gender = mapping.gender if mapping else None
    m_age = mapping.age if mapping else None
    m_edu = mapping.education_level if mapping else None
    m_course = mapping.course if mapping else None
    m_year = mapping.year_of_study if mapping else None
    m_cgpa = mapping.cgpa if mapping else None
    m_marital = mapping.marital_status if mapping else None
    m_dep = mapping.depression if mapping else None
    m_anx = mapping.anxiety if mapping else None
    m_panic = mapping.panic_attack if mapping else None
    m_treat = mapping.specialist_treatment if mapping else None

    for _, row in df.iterrows():
        try:
            raw_time = extract_value_by_alias(row, "time_date", user_mapped_col=m_time)
            raw_gender = extract_value_by_alias(row, "gender", user_mapped_col=m_gender)
            raw_age = extract_value_by_alias(row, "age", user_mapped_col=m_age)
            raw_edu = extract_value_by_alias(row, "education_level", user_mapped_col=m_edu)
            edu_norm = normalize_education_level(raw_edu)
            raw_course = extract_value_by_alias(row, "course", user_mapped_col=m_course)
            raw_year = extract_value_by_alias(row, "year_of_study", user_mapped_col=m_year)
            raw_cgpa = extract_value_by_alias(row, "cgpa", user_mapped_col=m_cgpa)
            raw_marital = extract_value_by_alias(row, "marital_status", user_mapped_col=m_marital)
            raw_dep = extract_value_by_alias(row, "depression", user_mapped_col=m_dep, default="No")
            raw_anx = extract_value_by_alias(row, "anxiety", user_mapped_col=m_anx, default="No")
            raw_panic = extract_value_by_alias(row, "panic_attack", user_mapped_col=m_panic, default="No")
            raw_treat = extract_value_by_alias(row, "specialist_treatment", user_mapped_col=m_treat, default="No")

            try:
                age_val = int(raw_age) if raw_age is not None and str(raw_age).strip() != "" else 20
            except (ValueError, TypeError):
                age_val = 20

            # ตรวจสอบว่าข้อมูลแถวนี้มีอยู่ในฐานข้อมูลแล้วหรือไม่
            row_signature = make_record_signature(
                raw_time, raw_gender, age_val, edu_norm, raw_course, raw_year,
                raw_cgpa, raw_marital, raw_dep, raw_anx, raw_panic, raw_treat
            )

            if row_signature in existing_signatures:
                skipped_count += 1
                continue

            db_record = MentalHealthRecord(
                time_date=raw_time,
                gender=raw_gender,
                age=age_val,
                education_level=edu_norm,
                course=raw_course,
                year_of_study=raw_year,
                cgpa=raw_cgpa,
                marital_status=raw_marital,
                depression=raw_dep,
                anxiety=raw_anx,
                panic_attack=raw_panic,
                specialist_treatment=raw_treat
            )
            db.add(db_record)
            existing_signatures.add(row_signature)
            imported_count += 1
        except Exception as e:
            print(f"Skipping row due to error: {e}")
            skipped_count += 1
            continue

    if imported_count > 0:
        db.commit()

    if imported_count > 0 and skipped_count > 0:
        msg = f"นำเข้าข้อมูลใหม่สำเร็จ {imported_count} รายการ (ข้ามข้อมูลที่ซ้ำกับในระบบ {skipped_count} รายการ)"
    elif imported_count > 0:
        msg = f"นำเข้าข้อมูลใหม่สำเร็จจำนวน {imported_count} รายการ"
    else:
        msg = f"ไม่มีข้อมูลใหม่ที่ต้องนำเข้า (ข้อมูลทั้งหมด {skipped_count} รายการซ้ำกับที่มีอยู่ในฐานข้อมูลแล้ว)"

    return ImportCSVResponse(
        imported_count=imported_count,
        skipped_count=skipped_count,
        status="success",
        message=msg
    )


def import_csv_to_db(
    db: Session,
    csv_path: str = "student_mental_health.csv",
    mapping: Optional[CSVColumnMapping] = None
) -> ImportCSVResponse:
    """
    อ่านไฟล์ CSV จาก Path ที่กำหนด และนำเข้าลง MySQL
    """
    if not os.path.exists(csv_path):
        return ImportCSVResponse(
            imported_count=0,
            status="failed",
            message=f"ไม่พบไฟล์ CSV ที่ตำแหน่ง: {csv_path}"
        )
    df = pd.read_csv(csv_path)
    return process_df_to_db(db, df, mapping=mapping)


def import_uploaded_csv_to_db(
    db: Session,
    file_contents: bytes,
    mapping: Optional[CSVColumnMapping] = None
) -> ImportCSVResponse:
    """
    นำเข้าไฟล์ CSV ที่ผู้ใช้อัปโหลดผ่าน API Upload File พร้อม Column Mapping
    """
    df = pd.read_csv(io.BytesIO(file_contents))
    return process_df_to_db(db, df, mapping=mapping)
