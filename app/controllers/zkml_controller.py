"""
ZK-ML Controller - Zero-Knowledge Machine Learning API Endpoints
"""

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import StudentFeatures, ZKMLResult
from app.models.ml_model import load_model_weights
from app.services.zk_service import execute_zkml_inference, get_student_sample_zk

router = APIRouter()


@router.get('/api/v1/zkml/model-info', tags=["ZK-ML Model"])
def get_model_info():
    """
    ดึงข้อมูลพารามิเตอร์ของโมเดล ML, Quantized Weights, Bias และค่า Accuracy
    """
    return load_model_weights()


@router.post('/api/v1/zkml/inference', response_model=ZKMLResult, tags=["ZK-ML Inference"])
async def run_inference(features: StudentFeatures):
    """
    ส่งข้อมูลสุขภาพจิตนักเรียนเพื่อประมวลผล ZK-ML Inference บน Noir ZK Circuit
    - ข้อมูลส่วนบุคคลจะถูกเก็บเป็น **Private Input** ไม่ส่งคืนใน Response
    - ส่งคืนเฉพาะผลลัพธ์การยืนยัน ZK Proof และระดับความเสี่ยง
    """
    try:
        result = await execute_zkml_inference(features)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการประมวลผล ZK-ML: {str(e)}"
        )


@router.get('/get-zpk', tags=["Sample Testing"])
async def get_zpk(count_student: int = 1):
    """
    ทดสอบดึงข้อมูลนักเรียนจากชุดข้อมูลสุ่มเพื่อรัน ZK-ML Inference
    """
    results = await get_student_sample_zk(count_student)
    return {
        "data": results,
        "message": "ประมวลผล ZK-ML Inference สำหรับข้อมูลตัวอย่างเรียบร้อยแล้ว",
        "status": 200
    }
