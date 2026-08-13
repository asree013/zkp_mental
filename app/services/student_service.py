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
from app.models.schemas import MentalHealthCreate, ImportCSVResponse, CSVColumnMapping

# ตารางชื่อเรียกคอลัมน์พัวพันหลายรูปแบบ (Column Aliases Mapping)
COLUMN_ALIASES = {
    "time_date": ["timestamp", "time_date", "time", "date", "created_at"],
    "gender": ["choose your gender", "gender", "sex"],
    "age": ["age", "student_age"],
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
    ดึงรายการข้อมูลสุขภาพจิตนักเรียนจาก MySQL Database
    """
    return db.query(MentalHealthRecord).offset(skip).limit(limit).all()


def process_df_to_db(
    db: Session,
    df: pd.DataFrame,
    mapping: Optional[CSVColumnMapping] = None
) -> ImportCSVResponse:
    """
    แปลงข้อมูลจาก Pandas DataFrame ลงตาราง mental_health_records โดยใช้ User Mapping หรือ Dynamic Aliases
    """
    count = 0
    m_time = mapping.time_date if mapping else None
    m_gender = mapping.gender if mapping else None
    m_age = mapping.age if mapping else None
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
            raw_age = extract_value_by_alias(row, "age", user_mapped_col=m_age)
            try:
                age_val = int(raw_age) if raw_age is not None else 20
            except (ValueError, TypeError):
                age_val = 20

            db_record = MentalHealthRecord(
                time_date=extract_value_by_alias(row, "time_date", user_mapped_col=m_time),
                gender=extract_value_by_alias(row, "gender", user_mapped_col=m_gender),
                age=age_val,
                course=extract_value_by_alias(row, "course", user_mapped_col=m_course),
                year_of_study=extract_value_by_alias(row, "year_of_study", user_mapped_col=m_year),
                cgpa=extract_value_by_alias(row, "cgpa", user_mapped_col=m_cgpa),
                marital_status=extract_value_by_alias(row, "marital_status", user_mapped_col=m_marital),
                depression=extract_value_by_alias(row, "depression", user_mapped_col=m_dep, default="No"),
                anxiety=extract_value_by_alias(row, "anxiety", user_mapped_col=m_anx, default="No"),
                panic_attack=extract_value_by_alias(row, "panic_attack", user_mapped_col=m_panic, default="No"),
                specialist_treatment=extract_value_by_alias(row, "specialist_treatment", user_mapped_col=m_treat, default="No")
            )
            db.add(db_record)
            count += 1
        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

    db.commit()
    return ImportCSVResponse(
        imported_count=count,
        status="success",
        message=f"นำเข้าข้อมูลลง MySQL Database สำเร็จจำนวน {count} รายการ"
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
