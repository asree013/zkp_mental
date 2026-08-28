"""
ZK-ML Controller - Zero-Knowledge Machine Learning API Endpoints
"""

from fastapi import APIRouter, HTTPException, Request, status
from app.models.schemas import StudentFeatures, ZKMLResult, RuleBasedZKResult, ZKComparisonResult
from app.models.ml_model import load_model_weights
from app.services.zk_service import (
    execute_zkml_inference,
    execute_rule_based_zk,
    execute_zk_comparison,
    get_student_sample_zk
)
from app.config.limiter import limiter

router = APIRouter()


@router.get('/api/v1/zkml/model-info', tags=["ZK-ML Model"])
@limiter.limit("60/minute")
def get_model_info(request: Request):
    """
    ดึงข้อมูลพารามิเตอร์ของโมเดล ML, Quantized Weights, Bias และค่า Accuracy
    """
    return load_model_weights()


@router.post('/api/v1/zkml/inference', response_model=ZKMLResult, tags=["ZK-ML Inference"])
@limiter.limit("30/minute")
async def run_inference(request: Request, features: StudentFeatures):
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


@router.post('/api/v1/zk/rule-based/inference', response_model=RuleBasedZKResult, tags=["Plain ZKP (Non-ML)"])
@limiter.limit("30/minute")
async def run_rule_based_inference(request: Request, features: StudentFeatures):
    """
    [Baseline Comparison API] รัน Zero-Knowledge Proof แบบธรรมดา (ไม่มี ML / กฎเกณฑ์คงที่)
    - ใช้ประเมินเปรียบเทียบคุณค่างานวิจัยว่าการใช้กฎเกณฑ์นับจำนวนทั่วไปมีข้อจำกัดอย่างไร
    - ไม่มีการใช้น้ำหนักโมเดลทางสถิติ (Unweighted Symptom Counting)
    """
    try:
        result = await execute_rule_based_zk(features)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการประมวลผล Plain ZK: {str(e)}"
        )


@router.post('/api/v1/zk/comparison', response_model=ZKComparisonResult, tags=["ZK vs ZK-ML Benchmark"])
@limiter.limit("30/minute")
async def run_zk_comparison(request: Request, features: StudentFeatures):
    """
    [Research Benchmark API] เปรียบเทียบผลลัพธ์ระหว่าง Plain ZKP (Non-ML) กับ ZK-ML แบบ Side-by-Side
    - ชี้ให้เห็นความแตกต่างด้านผลการตัดสินใจ, การคำนวณสหสัมพันธ์หลายมิติ, และคุณค่าทางวิชาการ
    """
    try:
        result = await execute_zk_comparison(features)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"เกิดข้อผิดพลาดในการรัน ZK Comparison: {str(e)}"
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

