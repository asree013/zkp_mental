"""
Research Paper & PDF Upload Controller
======================================
Controller สำหรับการอัปโหลดไฟล์ PDF งานวิจัย/วิทยานิพนธ์ (บทที่ 1-5, โครงร่าง, ข้อเสนอแนะ)
การจัดการ Metadata (เพิ่ม ลบ แก้ไข ดึงข้อมูล) ในฐานข้อมูล MySQL
พร้อมหน้า UI สำหรับจัดการเอกสารงานวิจัยที่ URL /paper
"""

import os
import re
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status, Request, Query, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config.database import get_db, check_db_connection
from app.models.db_models import ResearchPaper
from app.services.crypto_service import encrypt_bytes, decrypt_bytes
from app.models.schemas import (
    PaperType,
    PDFUploadResponse,
    ResearchPaperCreate,
    ResearchPaperUpdate,
    ResearchPaperResponse
)

router = APIRouter(tags=["Research Papers & PDF Uploads"])

# Template engine setup
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Upload directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal and illegal characters."""
    clean_name = os.path.basename(filename)
    clean_name = re.sub(r"[^\w\-_\.]", "_", clean_name)
    return clean_name or "document.pdf"


# =========================================================================
# WEB UI ROUTE (/paper)
# =========================================================================

@router.get("/paper", response_class=HTMLResponse, summary="Research Papers Management Web UI")
async def paper_management_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    หน้าเว็บ UI สำหรับจัดการไฟล์เอกสารงานวิจัย/วิทยานิพนธ์:
    - อัปโหลดไฟล์ PDF (บทที่ 1-5, เล่มเต็ม, โครงร่าง, ข้อเสนอแนะ)
    - แสดงรายการไฟล์ ค้นหา กรองประเภท
    - พรีวิว/เปิดอ่านเอกสาร PDF
    - แก้ไขชื่อและประเภทเอกสาร
    - ลบเอกสาร
    """
    db_status = check_db_connection()
    papers = []
    try:
        if db_status.get("status") == "connected":
            papers = db.query(ResearchPaper).order_by(ResearchPaper.id.desc()).all()
    except Exception as e:
        print(f"⚠️ Warning: Could not query research papers from database: {e}")

    return templates.TemplateResponse(
        request=request,
        name="paper.html",
        context={
            "db_status": db_status,
            "papers": papers,
            "active_page": "paper"
        }
    )




# =========================================================================
# REST API ENDPOINTS
# =========================================================================

def get_request_base_url(request: Request) -> str:
    """
    ดึง Base URL ที่รองรับทั้ง Localhost และ Production (Caddy / Nginx Reverse Proxy / HTTPS)
    1. ตรวจสอบ APP_BASE_URL จาก .env ก่อนเป็นลำดับแรก (เช่น https://zk-ml.yeedev.asia)
    2. หากไม่มี ให้ตรวจจับจาก Headers X-Forwarded-Proto / X-Forwarded-Host จาก Reverse Proxy
    3. Fallback ไปที่ request.base_url
    """
    env_base_url = os.getenv("APP_BASE_URL")
    if env_base_url and env_base_url.strip():
        return env_base_url.strip().rstrip("/")

    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    host = request.headers.get("x-forwarded-host", request.headers.get("host", ""))
    if host:
        return f"{proto}://{host}".rstrip("/")

    return str(request.base_url).rstrip("/")


@router.post("/api/upload/pdf", response_model=PDFUploadResponse, summary="Upload Research Paper PDF")
@router.post("/api/v1/papers/upload", response_model=PDFUploadResponse, summary="Upload Research Paper PDF (v1)")
async def upload_pdf_file(
    request: Request,
    file: UploadFile = File(..., description="ไฟล์ PDF งานวิจัย/วิทยานิพนธ์"),
    type_paper: Optional[PaperType] = Form(None, description="ประเภทเอกสาร (chapter_1..chapter_5, all_paper, proposal, recommend)"),
    custom_name: Optional[str] = Form(None, description="กำหนดชื่อไฟล์เอกสารเอง (ถ้าไม่ระบุจะใช้ชื่อไฟล์เดิม)"),
    save_to_db: bool = Form(True, description="บันทึกลงตาราง research_papers อัตโนมัติหรือไม่"),
    db: Session = Depends(get_db)
):
    """
    API สำหรับอัปโหลดไฟล์ PDF งานวิจัย:
    - บันทึกไฟล์ลงในโฟลเดอร์ `./uploads`
    - ตั้งชื่อไฟล์ตามเวลาของเครื่องคอมพิวเตอร์ที่อัปโหลดไฟล์ (Timestamp)
    - ส่งคืน Link ที่สามารถเรียกเปิด/ดาวน์โหลดไฟล์ได้ (รองรับทั้ง Localhost และ Production Domain)
    - บันทึกลงฐานข้อมูลตาราง `research_papers`
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ไม่พบชื่อไฟล์ กรุณาเลือกไฟล์ PDF ที่ต้องการอัปโหลด"
        )

    # ตรวจสอบว่าเป็นไฟล์ PDF หรือไม่
    original_filename = file.filename
    if not original_filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ระบบรองรับเฉพาะไฟล์เอกสารประเภท PDF (.pdf) เท่านั้น"
        )

    now = datetime.now(timezone.utc)
    timestamp_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = sanitize_filename(original_filename)
    saved_filename = f"{timestamp_prefix}_{clean_name}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    # เข้ารหัสไฟล์ (AES-256 Fernet Encryption at Rest) ก่อนบันทึกลงโฟลเดอร์ ./uploads
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ไฟล์ที่อัปโหลดมีขนาด 0 ไบต์ (Empty file)"
            )

        encrypted_contents = encrypt_bytes(contents)
        with open(file_path, "wb") as f:
            f.write(encrypted_contents)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการบันทึกและเข้ารหัสไฟล์: {str(e)}"
        )

    # สร้าง URL Link สำหรับเข้าถึงไฟล์ (รองรับ Reverse Proxy และ Production Base URL)
    base_url = get_request_base_url(request)
    file_link = f"{base_url}/uploads/{saved_filename}"
    display_name = custom_name.strip() if (custom_name and custom_name.strip()) else original_filename

    # บันทึก metadata ลง Database หากระบุ save_to_db=True
    if save_to_db:
        paper_type_val = type_paper.value if type_paper else "proposal"
        # normalize aliases
        if paper_type_val == "proposol":
            paper_type_val = "proposal"
        elif paper_type_val == "recomment":
            paper_type_val = "recommend"

        try:
            # เก็บ Relative URL (/uploads/...) ในฐานข้อมูล เพื่อให้ทำงานได้ทั้ง Localhost และ Production Domain โดยไม่ต้องแก้ข้อมูลใน DB
            db_relative_link = f"/uploads/{saved_filename}"
            db_paper = ResearchPaper(
                type_paper=paper_type_val,
                name=display_name,
                link=db_relative_link,
                file_type="pdf",
                create_date=now,
                update_date=now
            )
            db.add(db_paper)
            db.commit()
            db.refresh(db_paper)
        except Exception as e:
            db.rollback()
            print(f"⚠️ Warning: Could not save paper record to DB: {e}")


    return PDFUploadResponse(
        name_file=display_name,
        link=file_link,
        type="pdf",
        create_date=now,
        update_date=now
    )


@router.post("/api/v1/papers/records", response_model=ResearchPaperResponse, status_code=status.HTTP_201_CREATED, summary="Create Paper Record")
def create_paper_record(
    payload: ResearchPaperCreate,
    db: Session = Depends(get_db)
):
    """สร้างรายการเอกสารงานวิจัยในฐานข้อมูลแบบกำหนด Link เอง"""
    now = datetime.now(timezone.utc)
    paper_type_val = payload.type_paper.value
    if paper_type_val == "proposol":
        paper_type_val = "proposal"
    elif paper_type_val == "recomment":
        paper_type_val = "recommend"

    db_paper = ResearchPaper(
        type_paper=paper_type_val,
        name=payload.name,
        link=payload.link,
        file_type=payload.file_type or "pdf",
        create_date=now,
        update_date=now
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


@router.get("/api/v1/papers/records", response_model=List[ResearchPaperResponse], summary="List Research Papers")
def list_paper_records(
    type_paper: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """ดึงรายการเอกสารงานวิจัยทั้งหมดในระบบ (สามารถกรองตามประเภทเอกสารได้)"""
    query = db.query(ResearchPaper)
    if type_paper and type_paper.lower() != "all":
        query = query.filter(ResearchPaper.type_paper == type_paper)
    return query.order_by(ResearchPaper.id.desc()).all()


@router.get("/api/v1/papers/records/{paper_id}", response_model=ResearchPaperResponse, summary="Get Research Paper By ID")
def get_paper_record(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """ดึงข้อมูลเอกสารงานวิจัยตาม ID"""
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ไม่พบเอกสารงานวิจัย ID #{paper_id}"
        )
    return paper


@router.put("/api/v1/papers/records/{paper_id}", response_model=ResearchPaperResponse, summary="Update Research Paper")
@router.patch("/api/v1/papers/records/{paper_id}", response_model=ResearchPaperResponse, summary="Patch Research Paper")
def update_paper_record(
    paper_id: int,
    payload: ResearchPaperUpdate,
    db: Session = Depends(get_db)
):
    """
    แก้ไขข้อมูลเอกสารงานวิจัย (เปลี่ยนชื่อ หรือเปลี่ยนประเภทเอกสาร)
    """
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ไม่พบเอกสารงานวิจัย ID #{paper_id}"
        )

    if payload.name is not None and payload.name.strip():
        paper.name = payload.name.strip()

    if payload.type_paper is not None:
        type_val = payload.type_paper.value
        if type_val == "proposol":
            type_val = "proposal"
        elif type_val == "recomment":
            type_val = "recommend"
        paper.type_paper = type_val

    paper.update_date = datetime.now(timezone.utc)
    db.commit()
    db.refresh(paper)
    return paper


DELETE_AUTH_PASSWORD = os.getenv("DELETE_AUTH_PASSWORD", "P@ssw0rd")


@router.delete("/api/v1/papers/records/{paper_id}", summary="Delete Research Paper Record")
def delete_paper_record(
    paper_id: int,
    pass_for_delete: str = Query(..., description="รหัสผ่านความปลอดภัยสำหรับยืนยันการลบไฟล์เอกสาร"),
    delete_file: bool = Query(True, description="ลบไฟล์ PDF จริงออกจากดิสก์ด้วยหรือไม่"),
    db: Session = Depends(get_db)
):
    """
    ลบรายการเอกสารงานวิจัยและไฟล์ออกจากระบบ (ต้องระบุรหัสผ่านความปลอดภัยที่ถูกต้อง)
    """
    if pass_for_delete != DELETE_AUTH_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="รหัสผ่านสำหรับลบข้อมูลไม่ถูกต้อง (Invalid pass_for_delete)"
        )

    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ไม่พบเอกสารงานวิจัย ID #{paper_id}"
        )

    # พยายามลบไฟล์จริงออกจาก ./uploads
    if delete_file and paper.link:
        filename = paper.link.split("/")[-1]
        local_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(local_path):
            try:
                os.remove(local_path)
            except Exception as e:
                print(f"⚠️ Warning: Could not remove local file {local_path}: {e}")

    db.delete(paper)
    db.commit()
    return {
        "status": "success",
        "message": f"ลบเอกสาร ID #{paper_id} ('{paper.name}') และไฟล์ในระบบเรียบร้อยแล้ว"
    }


# =========================================================================
# SECURE ON-THE-FLY DECRYPTION STREAMING ENDPOINT
# =========================================================================

@router.get("/uploads/{filename}", summary="Download / View Decrypted Research Paper")
@router.get("/images/{filename}", summary="Download / View Decrypted Asset")
async def serve_decrypted_file(
    filename: str,
    download: bool = Query(False, description="ดาวน์โหลดเป็น Attachment หรือเปิดดูแบบ Inline ใน Browser")
):
    """
    ดึงไฟล์ที่ถูกเข้ารหัสไว้บนดิสก์เซิร์ฟเวอร์ (AES-256 Fernet Encryption at Rest)
    และทำการถอดรหัสแบบ On-the-fly ในหน่วยความจำ (RAM) เพื่อส่งให้ผู้ใช้เปิดอ่าน/ดาวน์โหลด
    โดยไม่มีการเขียนไฟล์ Plaintext ค้างไว้บนดิสก์
    """
    clean_name = sanitize_filename(filename)
    file_path = os.path.join(UPLOAD_DIR, clean_name)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ไม่พบไฟล์ {clean_name} บนเซิร์ฟเวอร์"
        )

    try:
        with open(file_path, "rb") as f:
            raw_encrypted_data = f.read()

        decrypted_data = decrypt_bytes(raw_encrypted_data)

        # วิเคราะห์ Content-Type ตามนามสกุลไฟล์
        lower_name = clean_name.lower()
        if lower_name.endswith(".pdf"):
            media_type = "application/pdf"
        elif lower_name.endswith(".png"):
            media_type = "image/png"
        elif lower_name.endswith(".jpg") or lower_name.endswith(".jpeg"):
            media_type = "image/jpeg"
        elif lower_name.endswith(".svg"):
            media_type = "image/svg+xml"
        elif lower_name.endswith(".txt"):
            media_type = "text/plain; charset=utf-8"
        else:
            media_type = "application/octet-stream"

        disposition = "attachment" if download else "inline"
        headers = {
            "Content-Disposition": f'{disposition}; filename="{clean_name}"',
            "Cache-Control": "private, max-age=3600",
            "X-Content-Type-Options": "nosniff"
        }

        return Response(content=decrypted_data, media_type=media_type, headers=headers)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการอ่านหรือถอดรหัสไฟล์: {str(e)}"
        )
