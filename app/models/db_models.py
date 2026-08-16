"""
Database ORM Models - SQLAlchemy Model Definitions
==================================================
ตาราง mental_health_records สำหรับเก็บข้อมูลแบบสำรวจสุขภาพจิตของนักเรียน
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
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


class ExperimentBenchmarkLog(Base):
    """
    SQLAlchemy Model สำหรับตาราง experiment_benchmark_logs
    เก็บบันทึกประวัติและผลการทดลองวิจัย ป.โท (Quantization & Cryptographic Benchmarks)
    """
    __tablename__ = "experiment_benchmark_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    benchmark_type = Column(String(50), nullable=False, index=True, comment="ประเภทการทดลอง (quantization, cryptographic)")
    dataset_source = Column(String(100), nullable=True, comment="แหล่งที่มาข้อมูล (MySQL Database, CSV Fallback)")
    total_samples = Column(Integer, nullable=True, comment="จำนวนตัวอย่างข้อมูลที่ใช้ทดสอบ")
    model_accuracy = Column(String(50), nullable=True, comment="ความแม่นยำของโมเดล (%)")
    optimal_scaling_factor = Column(Integer, nullable=True, comment="Scaling Factor ที่เหมาะสม (เช่น 1000)")
    acir_opcodes = Column(Integer, nullable=True, comment="จำนวน ACIR Circuit Constraints")
    mean_latency_ms = Column(String(50), nullable=True, comment="เวลาเฉลี่ยในการสร้าง Proof (ms)")
    p95_latency_ms = Column(String(50), nullable=True, comment="95th Percentile Latency (ms)")
    details_json = Column(Text, nullable=False, comment="ผลการทดลองแบบละเอียดในรูปแบบ JSON (Long Text)")
    created_at = Column(DateTime, default=datetime.utcnow, comment="เวลาที่ทำการทดลองและบันทึกผล")
    execution_note = Column(String(255), nullable=True, comment="บันทึกช่วยจำการทดลอง (Experiment Note)")
