"""
Database ORM Models - SQLAlchemy Model Definitions
==================================================
ตาราง mental_health_records สำหรับเก็บข้อมูลแบบสำรวจสุขภาพจิตของนักเรียน
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.config.database import Base


class MentalHealthRecord(Base):
    """
    SQLAlchemy Model สำหรับตาราง mental_health_records
    """
    __tablename__ = "mental_health_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_date = Column(String(100), nullable=True, comment="Timestamp จากแบบสำรวจ")
    gender = Column(String(50), nullable=True, comment="เพศ (Female, Male)")
    age = Column(Integer, nullable=True, comment="อายุ")
    course = Column(String(255), nullable=True, comment="สาขาวิชา/คณะ")
    year_of_study = Column(String(50), nullable=True, comment="ชั้นปีการศึกษา")
    cgpa = Column(String(50), nullable=True, comment="ช่วงเกรดเฉลี่ยสะสม CGPA")
    marital_status = Column(String(50), nullable=True, comment="สถานภาพสมรส")
    depression = Column(String(50), nullable=True, comment="ภาวะซึมเศร้า (Yes, No)")
    anxiety = Column(String(50), nullable=True, comment="ภาวะวิตกกังวล (Yes, No)")
    panic_attack = Column(String(50), nullable=True, comment="ภาวะแพนิค (Yes, No)")
    specialist_treatment = Column(String(50), nullable=True, comment="การเคยพบผู้เชี่ยวชาญ (Yes, No)")
    create_date = Column(DateTime, default=datetime.utcnow, comment="เวลาบันทึกข้อมูลลงฐานข้อมูล")
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="เวลาแก้ไขข้อมูลล่าสุด")
