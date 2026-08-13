"""
Student Controller - Student Mental Health DB & CSV Import Routes
==================================================================
"""

import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.schemas import MentalHealthCreate, MentalHealthResponse, ImportCSVResponse, CSVColumnMapping
from app.services.student_service import (
    create_mental_health_record,
    get_mental_health_records,
    import_csv_to_db,
    import_uploaded_csv_to_db
)

router = APIRouter(prefix="/api/v1/students", tags=["Student Mental Health Data"])


@router.post("/records", response_model=MentalHealthResponse, status_code=status.HTTP_201_CREATED)
def create_record(record: MentalHealthCreate, db: Session = Depends(get_db)):
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


@router.get("/records", response_model=List[MentalHealthResponse])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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


@router.post("/import-csv", response_model=ImportCSVResponse)
def import_csv(
    mapping: Optional[CSVColumnMapping] = Body(None, description="User Defined CSV Column Mapping Body"),
    db: Session = Depends(get_db)
):
    """
    นำเข้าข้อมูลจากไฟล์ student_mental_health.csv บนเซิร์ฟเวอร์เข้าสู่ MySQL Database
    - ผู้ใช้สามารถส่ง JSON Request Body เพื่อกำหนดชื่อ Column Mapping ใน CSV เองได้
    """
    try:
        result = import_csv_to_db(db, mapping=mapping)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการนำเข้าไฟล์ CSV: {str(e)}"
        )


@router.post("/upload-csv", response_model=ImportCSVResponse)
async def upload_csv(
    file: UploadFile = File(..., description="ไฟล์ CSV สำหรับอัปโหลด (.csv)"),
    time_date: Optional[str] = Form("Timestamp", description="ชื่อคอลัมน์ใน CSV สำหรับ Timestamp/Date"),
    gender: Optional[str] = Form("Choose your gender", description="ชื่อคอลัมน์ใน CSV สำหรับ Gender"),
    age: Optional[str] = Form("Age", description="ชื่อคอลัมน์ใน CSV สำหรับ Age"),
    course: Optional[str] = Form("What is your course?", description="ชื่อคอลัมน์ใน CSV สำหรับ Course"),
    year_of_study: Optional[str] = Form("Your current year of Study", description="ชื่อคอลัมน์ใน CSV สำหรับ Year of Study"),
    cgpa: Optional[str] = Form("What is your CGPA?", alias="CGPA", description="ชื่อคอลัมน์ใน CSV สำหรับ CGPA"),
    marital_status: Optional[str] = Form("Marital status", alias="marital", description="ชื่อคอลัมน์ใน CSV สำหรับ Marital status"),
    depression: Optional[str] = Form("Do you have Depression?", description="ชื่อคอลัมน์ใน CSV สำหรับ Depression"),
    anxiety: Optional[str] = Form("Do you have Anxiety?", description="ชื่อคอลัมน์ใน CSV สำหรับ Anxiety"),
    panic_attack: Optional[str] = Form("Do you have Panic attack?", description="ชื่อคอลัมน์ใน CSV สำหรับ Panic attack"),
    specialist_treatment: Optional[str] = Form("Did you seek any specialist for a treatment?", alias="Specialist_Treatment", description="ชื่อคอลัมน์ใน CSV สำหรับ Specialist Treatment"),
    mapping_json: Optional[str] = Form(None, description='หรือวาง JSON String ของ Mapping ตรงนี้ e.g. {"time_date": "Timestamp", "gender": "Choose your gender"}'),
    db: Session = Depends(get_db)
):
    """
    อัปโหลดและนำเข้าไฟล์ CSV ลง MySQL Database 
    - สามารถเลือกไฟล์ CSV และส่ง Column Mapping กำหนดชื่อคอลัมน์ใน CSV ไปพร้อมกันใน Request เดียวได้
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="รองรับเฉพาะไฟล์ประเภท .csv เท่านั้น"
        )

    mapping_obj = None

    # 1. ตรวจสอบว่ามีการวาง mapping_json มาหรือไม่
    if mapping_json:
        try:
            mapping_dict = json.loads(mapping_json)
            mapping_obj = CSVColumnMapping(**mapping_dict)
        except Exception as parse_err:
            print(f"Warning: Failed to parse mapping_json: {parse_err}")

    # 2. หากไม่มี mapping_json ให้ใช้ค่าพารามิเตอร์จาก Form
    if not mapping_obj:
        mapping_obj = CSVColumnMapping(
            time_date=time_date,
            gender=gender,
            age=age,
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
