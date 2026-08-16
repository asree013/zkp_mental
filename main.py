"""
Main Application Entry Point - FastAPI REST API System
======================================================
ระบบ REST API สำหรับการประมวลผล Zero-Knowledge Machine Learning (ZK-ML) บนข้อมูลสุขภาพจิตนักเรียน
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config.database import engine, Base
from app.models.db_models import MentalHealthRecord, ExperimentBenchmarkLog  # Import to register ORM models in Base.metadata
from app.models.ml_model import load_model_weights
from app.services.zk_service import get_nargo_bin
from app.controllers.home_controller import router as home_router
from app.controllers.health_controller import router as health_router
from app.controllers.zkml_controller import router as zkml_router
from app.controllers.student_controller import router as student_router
from app.controllers.benchmark_controller import router as benchmark_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # สร้างตารางใน MySQL อัตโนมัติหากยังไม่มี
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables verified / created successfully.")
    except Exception as e:
        print(f"⚠️ Could not connect to MySQL database during startup: {e}")

    model_data = load_model_weights()
    nargo_bin = get_nargo_bin()
    print("=========================================================")
    print("🚀 ZK-ML Mental Health FastAPI Server Is Running")
    print(f"🏠 Research Portal: http://localhost:8000/")
    print(f"📖 OpenAPI Docs: http://localhost:8000/docs")
    print(f"🔧 Nargo CLI Path: {nargo_bin}")
    print(f"🎯 ML Model Accuracy: {model_data.get('accuracy', 0) * 100:.2f}%")
    print("=========================================================")
    yield
    print("👋 Server is shutting down...")


from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from dotenv import load_dotenv
from app.config.limiter import limiter, custom_rate_limit_exceeded_handler

load_dotenv()

app = FastAPI(
    title="ZK-ML Student Mental Health API",
    description="REST API System for ZK-ML Inference on Student Mental Health Data (Privacy-Preserving Architecture)",
    version="1.0.0",
    lifespan=lifespan
)

# -------------------------------------------------------------------------
# CORS (Cross-Origin Resource Sharing) Configuration from .env
# -------------------------------------------------------------------------
cors_origins_raw = os.getenv("CORS_ORIGINS", "*")
if cors_origins_raw.strip() == "*":
    allow_origins = ["*"]
else:
    allow_origins = [origin.strip() for origin in cors_origins_raw.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Setup (SlowAPI)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Mount Static Files (Images, CSS, Assets)
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Register MVC Controller Routers
app.include_router(home_router)
app.include_router(health_router)
app.include_router(zkml_router)
app.include_router(student_router)
app.include_router(benchmark_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
