"""
Home Controller - Master's Thesis Portal & Researcher Dashboard
================================================================
หน้าแรก (Homepage /) แสดงโปรไฟล์ผู้วิจัย โครงสร้างวิทยานิพนธ์ และศูนย์ควบคุมระบบ ZK-ML
"""

import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models.ml_model import load_model_weights
from app.services.zk_service import get_nargo_bin
from app.config.database import check_db_connection

router = APIRouter(tags=["Home & Researcher Profile"])

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse, summary="Master's Thesis Research Portal Homepage")
async def home_page(request: Request):
    """
    เรนเดอร์หน้าแรก แสดงข้อมูลงานวิจัยวิทยานิพนธ์ โปรไฟล์ผู้วิจัย และระบบทดสอบ ZK-ML แบบโต้ตอบ
    """
    model_data = load_model_weights()
    db_status = check_db_connection()
    nargo_bin = get_nargo_bin()

    researcher_info = {
        "name_th": "นายอัสรี หะยีมะ",
        "name_en": "Asree Hayeema",
        "student_id": "6910025030",
        "year": "ชั้นปีที่ 1",
        "degree": "หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาวิทยาการข้อมูล (M.Sc. in Data Science - แผน ก แบบ ก 2)",
        "faculty": "โครงการจัดตั้งวิทยาลัยวิทยาศาสตร์ดิจิทัล สังกัดบัณฑิตวิทยาลัย",
        "profile_image": "/static/images/IMG_0457.JPG"
    }

    thesis_info = {
        "title_th": "การอนุมานโมเดลการเรียนรู้ของเครื่องแบบรักษาความเป็นส่วนตัวด้วยพยานหลักฐานความรู้เป็นศูนย์บนข้อมูลสุขภาพจิตนักเรียน",
        "title_en": "Privacy-Preserving Machine Learning Inference Using Zero-Knowledge Proofs on Student Mental Health Data",
        "model_accuracy": round(model_data.get("accuracy", 1.0) * 100, 2),
        "scaling_factor": model_data.get("scaling_factor", 1000),
        "db_status": db_status.get("status", "connected"),
        "nargo_path": nargo_bin
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "researcher": researcher_info,
            "thesis": thesis_info
        }
    )
