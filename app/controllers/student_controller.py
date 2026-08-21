"""
Student Controller - Student Mental Health DB & CSV Ingestion & UI Routes
========================================================================
ให้บริการทั้งหน้าเว็บ HTML (Jinja2) สำหรับจัดการข้อมูลนักเรียน และ REST API
"""

import os
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, Request, status, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config.database import get_db, check_db_connection
from app.models.schemas import MentalHealthCreate, MentalHealthResponse, ImportCSVResponse, CSVColumnMapping
from app.services.student_service import (
    create_mental_health_record,
    get_mental_health_records,
    get_student_statistics,
    delete_mental_health_record,
    clear_all_mental_health_records,
    import_csv_to_db,
    import_uploaded_csv_to_db
)

router = APIRouter(tags=["Student Mental Health Data & Management"])

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def _load_fallback_csv_records():
    """โหลดข้อมูลจำลองจาก student_mental_health.csv เมื่อ Database ยังไม่พร้อมใช้งาน"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "student_mental_health.csv")
    records = []
    if os.path.exists(csv_path):
        import pandas as pd
        try:
            df = pd.read_csv(csv_path)
            for idx, row in df.iterrows():
                try:
                    age_val = int(float(str(row.get("Age", "20"))))
                except Exception:
                    age_val = 20
                records.append({
                    "id": int(str(idx)) + 1,
                    "time_date": str(row.get("Timestamp", "")),
                    "gender": str(row.get("Choose your gender", "")),
                    "age": age_val,
                    "education_level": "UNK",
                    "course": str(row.get("What is your course?", "")),
                    "year_of_study": str(row.get("Your current year of Study", "")),
                    "cgpa": str(row.get("What is your CGPA?", "")),
                    "marital_status": str(row.get("Marital status", "")),
                    "depression": str(row.get("Do you have Depression?", "")),
                    "anxiety": str(row.get("Do you have Anxiety?", "")),
                    "panic_attack": str(row.get("Do you have Panic attack?", "")),
                    "specialist_treatment": str(row.get("Did you seek any specialist for a treatment?", ""))
                })
        except Exception as e:
            print(f"⚠️ Error reading fallback CSV: {e}")
    return records


def _calculate_fallback_stats(records_list):
    """คำนวณสถิติจากรายการข้อมูลนักเรียน"""
    total = len(records_list)
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
    dep_count = sum(1 for r in records_list if str(r.get("depression", "")).strip().lower() == "yes")
    anx_count = sum(1 for r in records_list if str(r.get("anxiety", "")).strip().lower() == "yes")
    panic_count = sum(1 for r in records_list if str(r.get("panic_attack", "")).strip().lower() == "yes")
    treat_count = sum(1 for r in records_list if str(r.get("specialist_treatment", "")).strip().lower() == "yes")
    high_risk_count = sum(1 for r in records_list if (
        str(r.get("depression", "")).strip().lower() == "yes" or
        str(r.get("anxiety", "")).strip().lower() == "yes" or
        str(r.get("panic_attack", "")).strip().lower() == "yes"
    ))
    return {
        "total_count": total,
        "depression_count": dep_count,
        "anxiety_count": anx_count,
        "panic_count": panic_count,
        "treatment_count": treat_count,
        "high_risk_count": high_risk_count,
        "low_risk_count": max(0, total - high_risk_count)
    }


# -------------------------------------------------------------------------
# 1. HTML Web Dashboard View
# -------------------------------------------------------------------------
@router.get("/students", response_class=HTMLResponse, summary="Student Data Management & CSV Ingestion Dashboard")
async def students_ui_page(request: Request, db: Session = Depends(get_db)):
    """
    เรนเดอร์หน้าเว็บ UI สำหรับจัดการข้อมูลสุขภาพจิตนักเรียน: เพิ่มข้อมูลรายคน, อัปโหลด CSV และดูตารางข้อมูล
    (รองรับ Hybrid Data Provider: แสดงผลได้ต่อเนื่องแม้ MySQL ยังไม่ได้เชื่อมต่อ)
    """
    db_status = check_db_connection()
    records_json = []
    stats = {
        "total_count": 0,
        "depression_count": 0,
        "anxiety_count": 0,
        "panic_count": 0,
        "treatment_count": 0,
        "high_risk_count": 0,
        "low_risk_count": 0
    }

    if db_status.get("status") == "connected":
        try:
            records = get_mental_health_records(db, skip=0, limit=1000)
            if records and len(records) > 0:
                stats = get_student_statistics(db)
                records_json = [
                    {
                        "id": r.id,
                        "time_date": r.time_date,
                        "gender": r.gender,
                        "age": r.age,
                        "education_level": r.education_level or "UNK",
                        "course": r.course,
                        "year_of_study": r.year_of_study,
                        "cgpa": r.cgpa,
                        "marital_status": r.marital_status,
                        "depression": r.depression,
                        "anxiety": r.anxiety,
                        "panic_attack": r.panic_attack,
                        "specialist_treatment": r.specialist_treatment
                    }
                    for r in records
                ]
            else:
                # DB ต่อได้แต่ยังไม่มีข้อมูลในตาราง ให้ดึงจาก CSV Fallback
                records_json = _load_fallback_csv_records()
                stats = _calculate_fallback_stats(records_json)
        except Exception as e:
            print(f"⚠️ Error querying students DB: {e}")
            records_json = _load_fallback_csv_records()
            stats = _calculate_fallback_stats(records_json)
    else:
        # DB ไม่ได้เชื่อมต่อ (Local dev without MySQL) ให้ใช้ CSV Fallback
        records_json = _load_fallback_csv_records()
        stats = _calculate_fallback_stats(records_json)

    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={
            "records": records_json,
            "records_json": records_json,
            "stats": stats,
            "db_status": db_status
        }
    )


from app.config.limiter import limiter

# -------------------------------------------------------------------------
# 2. REST API Endpoints
# -------------------------------------------------------------------------
@router.get("/api/v1/students/statistics", summary="Get Student Data Statistics Summary")
@limiter.limit("60/minute")
def read_student_stats(request: Request, db: Session = Depends(get_db)):
    """
    ดึงสรุปสถิติจำนวนนักเรียนและสัดส่วนความเสี่ยงสุขภาพจิตในฐานข้อมูล
    """
    db_status = check_db_connection()
    if db_status.get("status") == "connected":
        try:
            return get_student_statistics(db)
        except Exception as e:
            print(f"⚠️ Error getting DB statistics: {e}")
    
    fallback_records = _load_fallback_csv_records()
    return _calculate_fallback_stats(fallback_records)


@router.get("/api/v1/students/records", summary="Get List of Student Records")
@limiter.limit("60/minute")
def read_records(request: Request, skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    """
    ดึงรายการข้อมูลสุขภาพจิตนักเรียนจาก MySQL Database (พร้อม Hybrid Fallback)
    """
    db_status = check_db_connection()
    if db_status.get("status") == "connected":
        try:
            records = get_mental_health_records(db, skip=skip, limit=limit)
            return records
        except Exception as e:
            print(f"⚠️ Error querying records: {e}")
    
    fallback_records = _load_fallback_csv_records()
    return fallback_records[skip: skip + limit]


@router.post("/api/v1/students/records", response_model=MentalHealthResponse, status_code=status.HTTP_201_CREATED, summary="Create a Single Student Record")
@limiter.limit("30/minute")
def create_record(request: Request, record: MentalHealthCreate, db: Session = Depends(get_db)):
    """
    บันทึกข้อมูลสุขภาพจิตนักเรียน 1 รายการลง MySQL Database ผ่าน JSON Request Body
    """
    try:
        new_record = create_mental_health_record(db, record)
        return new_record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ไม่สามารถบันทึกข้อมูลลงฐานข้อมูลได้: {str(e)}"
        )


DELETE_AUTH_PASSWORD = os.getenv("DELETE_AUTH_PASSWORD", "P@ssw0rd")


@router.delete("/api/v1/students/records/{record_id}", summary="Delete Student Record by ID")
@limiter.limit("20/minute")
def delete_single_record(
    request: Request,
    record_id: int,
    pass_for_delete: str = Query(..., description="รหัสผ่านความปลอดภัยสำหรับยืนยันการลบข้อมูล"),
    db: Session = Depends(get_db)
):
    """
    ลบรายการข้อมูลนักเรียนตาม ID ที่ระบุ (ต้องระบุรหัสผ่านความปลอดภัยที่ถูกต้อง)
    """
    if pass_for_delete != DELETE_AUTH_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="รหัสผ่านสำหรับลบข้อมูลไม่ถูกต้อง (Invalid pass_for_delete)"
        )

    try:
        success = delete_mental_health_record(db, record_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ไม่พบข้อมูลนักเรียน ID {record_id} ในฐานข้อมูล"
            )
        return {"status": "success", "message": f"ลบข้อมูลนักเรียน ID #{record_id} เรียบร้อยแล้ว"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการลบข้อมูลจากฐานข้อมูล: {str(e)}"
        )


@router.delete("/api/v1/students/records", summary="Clear All Student Records")
@limiter.limit("5/minute")
def clear_all_records(
    request: Request,
    pass_for_delete: str = Query(..., description="รหัสผ่านความปลอดภัยสำหรับยืนยันการล้างข้อมูลทั้งหมด"),
    db: Session = Depends(get_db)
):
    """
    ล้างข้อมูลนักเรียนทั้งหมดในตาราง mental_health_records (ต้องระบุรหัสผ่านความปลอดภัยที่ถูกต้อง)
    """
    if pass_for_delete != DELETE_AUTH_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="รหัสผ่านสำหรับลบข้อมูลไม่ถูกต้อง (Invalid pass_for_delete)"
        )

    try:
        count = clear_all_mental_health_records(db)
        return {
            "status": "success",
            "message": f"ล้างข้อมูลนักเรียนทั้งหมดจำนวน {count} รายการเรียบร้อยแล้ว",
            "deleted_count": count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการล้างข้อมูลจากฐานข้อมูล: {str(e)}"
        )


@router.post("/api/v1/students/import-csv", response_model=ImportCSVResponse, summary="Import Default Server CSV to Database")
@limiter.limit("10/minute")
def import_csv(
    request: Request,
    mapping: Optional[CSVColumnMapping] = Body(None, description="User Defined CSV Column Mapping Body"),
    db: Session = Depends(get_db)
):
    """
    นำเข้าข้อมูลจากไฟล์ student_mental_health.csv บนเซิร์ฟเวอร์เข้าสู่ MySQL Database
    """
    try:
        result = import_csv_to_db(db, mapping=mapping)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการนำเข้าไฟล์ CSV: {str(e)}"
        )


@router.post("/api/v1/students/upload-csv", response_model=ImportCSVResponse, summary="Upload & Ingest CSV File to Database")
@limiter.limit("10/minute")
async def upload_csv(
    request: Request,
    file: UploadFile = File(..., description="ไฟล์ CSV สำหรับอัปโหลด (.csv)"),
    time_date: Optional[str] = Form("Timestamp", description="ชื่อคอลัมน์ใน CSV สำหรับ Timestamp/Date"),
    gender: Optional[str] = Form("Choose your gender", description="ชื่อคอลัมน์ใน CSV สำหรับ Gender"),
    age: Optional[str] = Form("Age", description="ชื่อคอลัมน์ใน CSV สำหรับ Age"),
    education_level: Optional[str] = Form("Education Level", description="ชื่อคอลัมน์ใน CSV สำหรับ Education Level"),
    course: Optional[str] = Form("What is your course?", description="ชื่อคอลัมน์ใน CSV สำหรับ Course"),
    year_of_study: Optional[str] = Form("Your current year of Study", description="ชื่อคอลัมน์ใน CSV สำหรับ Year of Study"),
    cgpa: Optional[str] = Form("What is your CGPA?", alias="CGPA", description="ชื่อคอลัมน์ใน CSV สำหรับ CGPA"),
    marital_status: Optional[str] = Form("Marital status", alias="marital", description="ชื่อคอลัมน์ใน CSV สำหรับ Marital status"),
    depression: Optional[str] = Form("Do you have Depression?", description="ชื่อคอลัมน์ใน CSV สำหรับ Depression"),
    anxiety: Optional[str] = Form("Do you have Anxiety?", description="ชื่อคอลัมน์ใน CSV สำหรับ Anxiety"),
    panic_attack: Optional[str] = Form("Do you have Panic attack?", description="ชื่อคอลัมน์ใน CSV สำหรับ Panic attack"),
    specialist_treatment: Optional[str] = Form("Did you seek any specialist for a treatment?", alias="Specialist_Treatment", description="ชื่อคอลัมน์ใน CSV สำหรับ Specialist Treatment"),
    mapping_json: Optional[str] = Form(None, description='หรือวาง JSON String ของ Mapping ตรงนี้'),
    db: Session = Depends(get_db)
):
    """
    อัปโหลดและนำเข้าไฟล์ CSV ลง MySQL Database พร้อม Column Mapping
    """
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="รองรับเฉพาะไฟล์ประเภท .csv เท่านั้น"
        )

    mapping_obj = None

    if mapping_json:
        try:
            mapping_dict = json.loads(mapping_json)
            mapping_obj = CSVColumnMapping(**mapping_dict)
        except Exception as parse_err:
            print(f"Warning: Failed to parse mapping_json: {parse_err}")

    if not mapping_obj:
        mapping_obj = CSVColumnMapping(
            time_date=time_date,
            gender=gender,
            age=age,
            education_level=education_level,
            course=course,
            year_of_study=year_of_study,
            CGPA=cgpa,
            marital=marital_status,
            depression=depression,
            anxiety=anxiety,
            panic_attack=panic_attack,
            Specialist_Treatment=specialist_treatment
        )

    try:
        contents = await file.read()
        res = import_uploaded_csv_to_db(db, contents, mapping=mapping_obj)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการอ่านและอัปโหลดไฟล์ CSV: {str(e)}"
        )
