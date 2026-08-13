from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class StudentFeatures(BaseModel):
    """Input payload for student mental health features."""
    age: int = Field(..., ge=15, le=100, description="Student age in years")
    cgpa_str: str = Field(..., description="CGPA range string, e.g., '3.50 - 4.00'")
    depression: int = Field(..., ge=0, le=1, description="1 if Depression present, 0 if No")
    anxiety: int = Field(..., ge=0, le=1, description="1 if Anxiety present, 0 if No")
    panic_attack: int = Field(..., ge=0, le=1, description="1 if Panic attack present, 0 if No")
    seek_treatment: int = Field(..., ge=0, le=1, description="1 if Sought specialist treatment, 0 if No")


class ZKMLResult(BaseModel):
    """Response payload for ZK-ML inference and verification result."""
    student_index: Optional[int] = Field(None, description="Index of student if running from sample dataset")
    verification_status: str = Field(..., description="'Pass' if proof generated & verified, otherwise 'Not Pass'")
    risk_class: int = Field(..., description="0 = Low Risk, 1 = High Risk / Welfare Support Recommended")
    risk_label: str = Field(..., description="Human-readable risk label")
    proving_time_ms: float = Field(..., description="Latency of ZK Proof execution in milliseconds")
    message: str = Field(..., description="Status summary message")


class HealthCheckResponse(BaseModel):
    """System health check payload."""
    status: str
    nargo_bin: str
    service: str
    database: Optional[Dict[str, Any]] = None


# -------------------------------------------------------------
# DATABASE RECORD SCHEMAS
# -------------------------------------------------------------

class MentalHealthCreate(BaseModel):
    """Schema สำหรับรับ JSON Body เพิ่มข้อมูลสุขภาพจิต 1 รายการลง DB"""
    time_date: Optional[str] = Field(None, alias="time_date", description="Timestamp จากแบบสำรวจ")
    gender: Optional[str] = Field(None, description="เพศ e.g. Female, Male")
    age: int = Field(..., ge=10, le=100, description="อายุ")
    course: Optional[str] = Field(None, description="สาขาวิชา/คณะ")
    year_of_study: Optional[str] = Field(None, description="ชั้นปีการศึกษา e.g. Year 1, year 2")
    cgpa: Optional[str] = Field(None, alias="CGPA", description="เกรดเฉลี่ยสะสม CGPA e.g. 3.50 - 4.00")
    marital_status: Optional[str] = Field(None, description="สถานภาพสมรส")
    depression: str = Field(..., description="ภาวะซึมเศร้า (Yes / No)")
    anxiety: str = Field(..., description="ภาวะวิตกกังวล (Yes / No)")
    panic_attack: str = Field(..., description="ภาวะแพนิค (Yes / No)")
    specialist_treatment: str = Field(..., alias="Specialist_Treatment", description="การเคยพบผู้เชี่ยวชาญ (Yes / No)")

    class Config:
        populate_by_name = True


class MentalHealthResponse(BaseModel):
    """Schema สำหรับส่งคืนข้อมูลจากตาราง mental_health_records"""
    id: int
    time_date: Optional[str] = None
    gender: Optional[str] = None
    age: int
    course: Optional[str] = None
    year_of_study: Optional[str] = None
    cgpa: Optional[str] = None
    marital_status: Optional[str] = None
    depression: str
    anxiety: str
    panic_attack: str
    specialist_treatment: str
    create_date: datetime
    update_date: datetime

    class Config:
        from_attributes = True


class CSVColumnMapping(BaseModel):
    """Schema สำหรับให้ User กำหนดชื่อ Column Mapping จากไฟล์ CSV เองใน Body"""
    time_date: Optional[str] = Field("Timestamp", description="ชื่อคอลัมน์ใน CSV สำหรับ Time/Date")
    gender: Optional[str] = Field("Choose your gender", description="ชื่อคอลัมน์ใน CSV สำหรับ Gender")
    age: Optional[str] = Field("Age", description="ชื่อคอลัมน์ใน CSV สำหรับ Age")
    course: Optional[str] = Field("What is your course?", description="ชื่อคอลัมน์ใน CSV สำหรับ Course")
    year_of_study: Optional[str] = Field("Your current year of Study", description="ชื่อคอลัมน์ใน CSV สำหรับ Year of Study")
    cgpa: Optional[str] = Field("What is your CGPA?", alias="CGPA", description="ชื่อคอลัมน์ใน CSV สำหรับ CGPA")
    marital_status: Optional[str] = Field("Marital status", alias="marital", description="ชื่อคอลัมน์ใน CSV สำหรับ Marital status")
    depression: Optional[str] = Field("Do you have Depression?", description="ชื่อคอลัมน์ใน CSV สำหรับ Depression")
    anxiety: Optional[str] = Field("Do you have Anxiety?", description="ชื่อคอลัมน์ใน CSV สำหรับ Anxiety")
    panic_attack: Optional[str] = Field("Do you have Panic attack?", description="ชื่อคอลัมน์ใน CSV สำหรับ Panic attack")
    specialist_treatment: Optional[str] = Field("Did you seek any specialist for a treatment?", alias="Specialist_Treatment", description="ชื่อคอลัมน์ใน CSV สำหรับ Specialist Treatment")

    class Config:
        populate_by_name = True


class ImportCSVResponse(BaseModel):
    """Schema ตอบกลับผลลัพธ์การนำเข้าไฟล์ CSV"""
    imported_count: int
    status: str
    message: str
