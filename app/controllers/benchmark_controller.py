"""
Benchmark Controller - Quantization Impact HTML View & REST API
================================================================
ให้บริการหน้าเว็บ HTML ผ่าน Jinja2 Template สำหรับแสดงผลการทดลองวิทยานิพนธ์
และ REST API JSON Data Endpoint
"""

import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.benchmark_service import get_quantization_benchmark_data

router = APIRouter(tags=["Quantization Benchmark"])

# กำหนด Path ของ Templates Folder
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/test-quantization-impact", response_class=HTMLResponse, summary="Quantization Impact Web Dashboard (Jinja2)")
async def view_quantization_impact(request: Request):
    """
    เรนเดอร์หน้าเว็บ HTML (Jinja2) สำหรับแสดงตารางเปรียบเทียบและกราฟผลกระทบของ Quantization
    """
    data = get_quantization_benchmark_data()
    return templates.TemplateResponse(
        request=request,
        name="quantization_impact.html",
        context={
            "baseline": data["baseline"],
            "rows": data["rows"],
            "chart_data": data["chart_data"]
        }
    )


@router.get("/api/v1/benchmark/quantization", summary="Quantization Benchmark Raw JSON Data")
async def get_quantization_json():
    """
    ส่งคืนข้อมูลผลการทดลอง Quantization ในรูปแบบ JSON API
    """
    return get_quantization_benchmark_data()
