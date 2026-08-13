"""
Controllers Layer - API Route Handlers
"""
from app.controllers.health_controller import router as health_router
from app.controllers.zkml_controller import router as zkml_router
from app.controllers.student_controller import router as student_router

__all__ = [
    "health_router",
    "zkml_router",
    "student_router"
]
