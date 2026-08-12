from typing import Optional
from pydantic import BaseModel, Field


class StudentFeatures(BaseModel):
    """Input payload for student mental health features."""
    age: int = Field(..., ge=15, le=100, description="Student age in years")
    cgpa_str: str = Field(..., description="CGPA range string, e.g., '3.50 - 4.00'")
    depression: int = Field(..., ge=0, le=1, description="1 if Depression present, 0 if No")
    anxiety: int = Field(..., ge=0, le=1, description="1 if Anxiety present, 0 if No")
    panic_attack: int = Field(..., ge=0, le=1, description="1 if Panic attack present, 0 if No")
    seek_treatment: int = Field(..., ge=0, le=1, description="1 if Sought specialist treatment, 0 if No")


class ZKMLResult(BaseModel):
    """Response payload for ZK-ML inference and verification result."""
    student_index: Optional[int] = Field(None, description="Index of student if running from sample dataset")
    verification_status: str = Field(..., description="'Pass' if proof generated & verified, otherwise 'Not Pass'")
    risk_class: int = Field(..., description="0 = Low Risk, 1 = High Risk / Welfare Support Recommended")
    risk_label: str = Field(..., description="Human-readable risk label")
    proving_time_ms: float = Field(..., description="Latency of ZK Proof execution in milliseconds")
    message: str = Field(..., description="Status summary message")


class HealthCheckResponse(BaseModel):
    """System health check payload."""
    status: str
    nargo_bin: str
    service: str
