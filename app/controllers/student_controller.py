"""
Student Controller - Student Mental Health DB & CSV Ingestion & UI Routes
========================================================================
ให้บริการทั้งหน้าเว็บ HTML (Jinja2) สำหรับจัดการข้อมูลนักเรียน และ REST API
"""

import os
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, Request, status
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


# -------------------------------------------------------------------------
# 1. HTML Web Dashboard View
# -------------------------------------------------------------------------
@router.get("/students", response_class=HTMLResponse, summary="Student Data Management & CSV Ingestion Dashboard")
async def students_ui_page(request: Request, db: Session = Depends(get_db)):
    """
    เรนเดอร์หน้าเว็บ UI สำหรับจัดการข้อมูลสุขภาพจิตนักเรียน: เพิ่มข้อมูลรายคน, อัปโหลด CSV และดูตารางข้อมูล
    """
    records = get_mental_health_records(db, skip=0, limit=1000)
    stats = get_student_statistics(db)
    db_status = check_db_connection()

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

    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={
            "records": records,
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
    return get_student_statistics(db)


@router.get("/api/v1/students/records", response_model=List[MentalHealthResponse], summary="Get List of Student Records")
@limiter.limit("60/minute")
def read_records(request: Request, skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    """
    ดึงรายการข้อมูลสุขภาพจิตนักเรียนจาก MySQL Database
    """
    try:
        records = get_mental_health_records(db, skip=skip, limit=limit)
        return records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการดึงข้อมูลจากฐานข้อมูล: {str(e)}"
        )


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


# =====================================================================
# DELETE Endpoints disabled for Security & Research Data Integrity
# =====================================================================
# @router.delete("/api/v1/students/records/{record_id}", summary="Delete Student Record by ID")
# def delete_single_record(record_id: int, db: Session = Depends(get_db)):
#     """
#     ลบรายการข้อมูลนักเรียนตาม ID ที่ระบุ
#     """
#     success = delete_mental_health_record(db, record_id)
#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"ไม่พบข้อมูลนักเรียน ID {record_id} ในฐานข้อมูล"
#         )
#     return {"status": "success", "message": f"ลบข้อมูล ID {record_id} เรียบร้อยแล้ว"}
#
#
# @router.delete("/api/v1/students/records", summary="Clear All Student Records")
# def clear_all_records(db: Session = Depends(get_db)):
#     """
#     ล้างข้อมูลนักเรียนทั้งหมดในตาราง mental_health_records
#     """
#     count = clear_all_mental_health_records(db)
#     return {"status": "success", "message": f"ล้างข้อมูลนักเรียนทั้งหมดจำนวน {count} รายการเรียบร้อยแล้ว"}


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
