"""
Health Controller - System Status & Health Check Routes
"""

from fastapi import APIRouter
from app.models.schemas import HealthCheckResponse
from app.services.zk_service import get_nargo_bin
from app.config.database import check_db_connection

router = APIRouter(tags=["System & Health"])


@router.get('/health', response_model=HealthCheckResponse)
def health_check():
    """
    ตรวจสอบสถานะความพร้อมของระบบ API, Nargo CLI และการเชื่อมต่อ MySQL Database จาก .env
    """
    db_status = check_db_connection()
    return HealthCheckResponse(
        status="healthy",
        nargo_bin=get_nargo_bin(),
        service="ZK-ML Student Mental Health API",
        database=db_status
    )
