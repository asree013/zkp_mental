"""
Database Configuration & SQLAlchemy Connection Module
======================================================
โหลดการตั้งค่าการเชื่อมต่อ MySQL Database จากไฟล์ .env
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# โหลดค่าตัวแปรสภาพแวดล้อมจากไฟล์ .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "default-db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")

# ดึงค่า DATABASE_URL หรือสร้างขึ้นตามพารามิเตอร์ที่อ่านได้จาก .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# สร้าง SQLAlchemy Connection Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

# SessionFactory สำหรับจัดการ Database Session ในแอปพลิเคชัน
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM Base Class
Base = declarative_base()


def init_db_schema():
    """
    สร้างตาราง และเพิ่มคอลัมน์ใหม่อัตโนมัติ (Auto Schema Migration)
    """
    try:
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            # ตรวจสอบว่ามีคอลัมน์ education_level ในตาราง mental_health_records หรือยัง
            check_col = conn.execute(text(
                "SELECT COUNT(*) FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA = :db_name AND TABLE_NAME = 'mental_health_records' AND COLUMN_NAME = 'education_level'"
            ), {"db_name": DB_NAME}).scalar()

            if check_col == 0:
                conn.execute(text(
                    "ALTER TABLE mental_health_records ADD COLUMN education_level VARCHAR(50) DEFAULT 'UNK' "
                    "COMMENT 'ระดับการศึกษา (PP, PE, LSE, USE_VS, BBDL, BD, MD, PHD, UNK)' AFTER age"
                ))
                conn.commit()
                print("✨ Auto-migrated: Added 'education_level' column to mental_health_records table.")
    except Exception as e:
        print(f"⚠️ init_db_schema note: {e}")


def check_db_connection() -> dict:
    """
    ฟังก์ชันตรวจสอบความพร้อมของการเชื่อมต่อ MySQL Database
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "database": DB_NAME,
            "host": f"{DB_HOST}:{DB_PORT}",
            "user": DB_USER
        }
    except Exception as e:
        return {
            "status": "disconnected",
            "error": str(e),
            "database": DB_NAME,
            "host": f"{DB_HOST}:{DB_PORT}"
        }


def get_db():
    """
    FastAPI Dependency สำหรับให้ Controllers ดึง Database Session ไปใช้งาน
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
