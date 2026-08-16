"""
Rate Limiter Configuration & Security Middleware (SlowAPI)
===========================================================
ระบบจำกัดอัตราการเรียกใช้งาน API (Rate Limiting) เพื่อป้องกัน:
1. การโจมตีแบบ DoS / DDoS / Brute-force
2. การยิงคำขอสร้าง ZK Proof ปริมาณมากเกินไปจน CPU ทำงานหนัก (Resource Exhaustion)
3. การสแปมนำเข้าหรือบันทึกข้อมูลนักเรียน
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Custom 429 Too Many Requests Exception Handler
    ส่งข้อความแจ้งเตือนภาษาไทยและภาษาอังกฤษอย่างชัดเจน
    """
    return JSONResponse(
        status_code=429,
        content={
            "status": "rate_limit_exceeded",
            "error_code": 429,
            "message": "คำขอใช้งานเกินขีดจำกัดความปลอดภัยของระบบ (Rate Limit Exceeded)",
            "detail": f"คุณส่งคำขอถี่เกินไป ({exc.detail}) กรุณารอสักครู่แล้วลองใหม่อีกครั้ง เพื่อความปลอดภัยของระบบวิจัย",
            "client_ip": request.client.host if request.client else "unknown"
        },
        headers={
            "Retry-After": "60"
        }
    )


# สร้าง Limiter Instance โดยใช้ IP Address ของผู้ส่งคำขอเป็น Key
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["120/minute"],  # ค่ามาตรฐานทั่วไป: 120 คำขอต่อนาทีต่อ 1 IP
    headers_enabled=False
)
