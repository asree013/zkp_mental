"""
Benchmark Controller - Quantization Impact HTML View & REST API
================================================================
ให้บริการหน้าเว็บ HTML ผ่าน Jinja2 Template สำหรับแสดงผลการทดลองวิทยานิพนธ์
และ REST API JSON Data Endpoint
"""

import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.benchmark_service import get_quantization_benchmark_data
from app.services.zk_benchmark_service import run_cryptographic_benchmark

router = APIRouter(tags=["Benchmarks (Thesis Research)"])

# กำหนด Path ของ Views Folder (MVC Architecture)
VIEWS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "views")
views = Jinja2Templates(directory=VIEWS_DIR)


# =========================================================================
# 1. Quantization Impact Benchmark
# =========================================================================

@router.get("/test-quantization-impact", summary="Legacy redirect to /en/test-quantization-impact default")
async def redirect_quantization_impact():
    """Redirect unlocalized path to /en/... (Default English)"""
    return RedirectResponse(url="/en/test-quantization-impact", status_code=307)


@router.get("/{lang}/test-quantization-impact", response_class=HTMLResponse, summary="1) Quantization Impact Web Dashboard (Jinja2)")
@router.get("/{lang}/test-quantization-impact/", response_class=HTMLResponse, include_in_schema=False)
async def view_quantization_impact(request: Request, lang: str = "en", force_refresh: bool = False):
    """
    เรนเดอร์หน้าเว็บ HTML (Jinja2) สำหรับแสดงตารางเปรียบเทียบและกราฟผลกระทบของ Quantization (รองรับ /th/ และ /en/)
    """
    if lang not in ["th", "en"]:
        return RedirectResponse(url="/en/test-quantization-impact", status_code=307)

    data = get_quantization_benchmark_data(force_refresh=force_refresh)
    return views.TemplateResponse(
        request=request,
        name="quantization_impact.html",
        context={
            "baseline": data["baseline"],
            "rows": data["rows"],
            "chart_data": data["chart_data"],
            "snapshot_info": data.get("snapshot_info", {}),
            "active_page": "quantization",
            "current_lang": lang,
            "lang": lang
        }
    )


@router.get("/api/v1/benchmark/quantization", summary="Quantization Benchmark Raw JSON Data")
async def get_quantization_json(force_refresh: bool = False):
    """
    ส่งคืนข้อมูลผลการทดลอง Quantization ในรูปแบบ JSON API
    """
    return get_quantization_benchmark_data(force_refresh=force_refresh)


# =========================================================================
# 2. Cryptographic Benchmark
# =========================================================================

@router.get("/test-cryptographic-benchmark", summary="Legacy redirect to /en/test-cryptographic-benchmark default")
async def redirect_cryptographic_benchmark():
    """Redirect unlocalized path to /en/... (Default English)"""
    return RedirectResponse(url="/en/test-cryptographic-benchmark", status_code=307)


@router.get("/{lang}/test-cryptographic-benchmark", response_class=HTMLResponse, summary="2) Cryptographic & ZK Performance Dashboard (Jinja2)")
@router.get("/{lang}/test-cryptographic-benchmark/", response_class=HTMLResponse, include_in_schema=False)
async def view_cryptographic_benchmark(request: Request, lang: str = "en", force_refresh: bool = False):
    """
    เรนเดอร์หน้าเว็บ HTML (Jinja2) สำหรับแสดงผล Cryptographic Benchmark (ACIR Opcodes, Constraints, Prover Latency) (รองรับ /th/ และ /en/)
    """
    if lang not in ["th", "en"]:
        return RedirectResponse(url="/en/test-cryptographic-benchmark", status_code=307)

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
            "snapshot_info": data.get("snapshot_info", {}),
            "active_page": "cryptographic",
            "current_lang": lang,
            "lang": lang
        }
    )


@router.get("/api/v1/benchmark/cryptographic", summary="Cryptographic Benchmark Raw JSON Data")
async def get_cryptographic_json(force_refresh: bool = False):
    """
    ส่งคืนข้อมูลผลการทดลอง Cryptographic Benchmark ในรูปแบบ JSON API
    """
    return await run_cryptographic_benchmark(iterations=25, force_refresh=force_refresh)


# =========================================================================
# 3. Compare ZKP vs ZK-ML
# =========================================================================

@router.get("/compare-zkp-zkml", summary="Legacy redirect to /en/compare-zkp-zkml default")
@router.get("/test-compare-zkp-zkml", include_in_schema=False)
async def redirect_compare_zkp_zkml():
    """Redirect unlocalized path to /en/... (Default English)"""
    return RedirectResponse(url="/en/compare-zkp-zkml", status_code=307)


@router.get("/{lang}/compare-zkp-zkml", response_class=HTMLResponse, summary="3) Compare Plain ZKP vs ZK-ML Research Value Dashboard (Jinja2)")
@router.get("/{lang}/compare-zkp-zkml/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/{lang}/test-compare-zkp-zkml", response_class=HTMLResponse, include_in_schema=False)
@router.get("/{lang}/test-compare-zkp-zkml/", response_class=HTMLResponse, include_in_schema=False)
async def view_compare_zkp_zkml(request: Request, lang: str = "en"):
    """
    เรนเดอร์หน้าเว็บ HTML (Jinja2) สำหรับแสดงผลเปรียบเทียบคุณค่างานวิจัยระหว่าง Plain ZKP vs ZK-ML (รองรับ /th/ และ /en/)
    """
    if lang not in ["th", "en"]:
        return RedirectResponse(url="/en/compare-zkp-zkml", status_code=307)

    from app.models.ml_model import load_model_weights
    from app.services.zk_service import get_nargo_bin

    model_info = load_model_weights()
    nargo_bin = get_nargo_bin()

    return views.TemplateResponse(
        request=request,
        name="compare_zkp_zkml.html",
        context={
            "model_info": model_info,
            "nargo_bin": nargo_bin,
            "active_page": "compare",
            "current_lang": lang,
            "lang": lang
        }
    )

