"""
Main Application Entry Point - FastAPI REST API System
======================================================
ระบบ REST API สำหรับการประมวลผล Zero-Knowledge Machine Learning (ZK-ML) บนข้อมูลสุขภาพจิตนักเรียน
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.models.ml_model import load_model_weights
from app.services.zk_service import get_nargo_bin
from app.controllers.health_controller import router as health_router
from app.controllers.zkml_controller import router as zkml_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_data = load_model_weights()
    nargo_bin = get_nargo_bin()
    print("=========================================================")
    print("🚀 ZK-ML Mental Health FastAPI Server Is Running")
    print(f"📖 OpenAPI Docs: http://localhost:8000/docs")
    print(f"🔧 Nargo CLI Path: {nargo_bin}")
    print(f"🎯 ML Model Accuracy: {model_data.get('accuracy', 0) * 100:.2f}%")
    print("=========================================================")
    yield
    print("👋 Server is shutting down...")


app = FastAPI(
    title="ZK-ML Student Mental Health API",
    description="REST API System for ZK-ML Inference on Student Mental Health Data (Privacy-Preserving Architecture)",
    version="1.0.0",
    lifespan=lifespan
)

# Redirect root to OpenAPI docs
@app.get('/', include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')

# Register MVC Controller Routers
app.include_router(health_router)
app.include_router(zkml_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
