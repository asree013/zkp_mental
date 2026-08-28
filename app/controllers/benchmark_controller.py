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
from app.services.zk_benchmark_service import run_cryptographic_benchmark

router = APIRouter(tags=["Benchmarks (Thesis Research)"])

# กำหนด Path ของ Views Folder (MVC Architecture)
VIEWS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "views")
views = Jinja2Templates(directory=VIEWS_DIR)


@router.get("/test-quantization-impact", response_class=HTMLResponse, summary="1) Quantization Impact Web Dashboard (Jinja2)")
async def view_quantization_impact(request: Request, force_refresh: bool = False):
    """
    เรนเดอร์หน้าเว็บ HTML (Jinja2) สำหรับแสดงตารางเปรียบเทียบและกราฟผลกระทบของ Quantization
    """
    data = get_quantization_benchmark_data(force_refresh=force_refresh)
    return views.TemplateResponse(
        request=request,
        name="quantization_impact.html",
        context={
            "baseline": data["baseline"],
            "rows": data["rows"],
            "chart_data": data["chart_data"],
            "snapshot_info": data.get("snapshot_info", {})
        }
    )


@router.get("/api/v1/benchmark/quantization", summary="Quantization Benchmark Raw JSON Data")
async def get_quantization_json(force_refresh: bool = False):
    """
    ส่งคืนข้อมูลผลการทดลอง Quantization ในรูปแบบ JSON API
    """
    return get_quantization_benchmark_data(force_refresh=force_refresh)


@router.get("/test-cryptographic-benchmark", response_class=HTMLResponse, summary="2) Cryptographic & ZK Performance Dashboard (Jinja2)")
async def view_cryptographic_benchmark(request: Request, force_refresh: bool = False):
    """
    เรนเดอร์หน้าเว็บ HTML (Jinja2) สำหรับแสดงผล Cryptographic Benchmark (ACIR Opcodes, Constraints, Prover Latency)
    """
    data = await run_cryptographic_benchmark(iterations=25, force_refresh=force_refresh)
    return views.TemplateResponse(
        request=request,
        name="cryptographic_benchmark.html",
        context={
            "summary": data["summary"],
            "circuit_breakdown": data["circuit_breakdown"],
            "scaling_data": data["scaling_data"],
            "iteration_series": data["iteration_series"],
            "iteration_labels": data["iteration_labels"],
            "scaling_chart": data["scaling_chart"],
            "snapshot_info": data.get("snapshot_info", {})
        }
    )


@router.get("/api/v1/benchmark/cryptographic", summary="Cryptographic Benchmark Raw JSON Data")
async def get_cryptographic_json(force_refresh: bool = False):
    """
    ส่งคืนข้อมูลผลการทดลอง Cryptographic Benchmark ในรูปแบบ JSON API
    """
    return await run_cryptographic_benchmark(iterations=25, force_refresh=force_refresh)


@router.get("/compare-zkp-zkml", response_class=HTMLResponse, summary="3) Compare Plain ZKP vs ZK-ML Research Value Dashboard (Jinja2)")
@router.get("/test-compare-zkp-zkml", response_class=HTMLResponse, include_in_schema=False)
async def view_compare_zkp_zkml(request: Request):
    """
    เรนเดอร์หน้าเว็บ HTML (Jinja2) สำหรับแสดงผลเปรียบเทียบคุณค่างานวิจัยระหว่าง Plain ZKP vs ZK-ML
    """
    from app.models.ml_model import load_model_weights
    from app.services.zk_service import get_nargo_bin

    model_info = load_model_weights()
    nargo_bin = get_nargo_bin()

    return views.TemplateResponse(
        request=request,
        name="compare_zkp_zkml.html",
        context={
            "model_info": model_info,
            "nargo_bin": nargo_bin
        }
    )

