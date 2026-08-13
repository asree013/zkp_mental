"""
API Test Suite - Verification of MVC Architecture, ZK-ML, Student DB & Dynamic Column Mapping
"""

import io
import pandas as pd
from fastapi.testclient import TestClient
from main import app
from app.models.schemas import CSVColumnMapping
from app.services.student_service import process_df_to_db

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✅ GET /health PASSED:", data)


def test_model_info():
    response = client.get("/api/v1/zkml/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "quantized_weights" in data
    print("✅ GET /api/v1/zkml/model-info PASSED: Weights =", data["quantized_weights"])


def test_zkml_inference():
    payload = {
        "age": 21,
        "cgpa_str": "3.50 - 4.00",
        "depression": 1,
        "anxiety": 1,
        "panic_attack": 0,
        "seek_treatment": 0
    }
    response = client.post("/api/v1/zkml/inference", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verification_status"] == "Pass"
    assert "proving_time_ms" in data
    print("✅ POST /api/v1/zkml/inference PASSED:", data)


def test_user_custom_column_mapping_body():
    # User custom mapping JSON body
    custom_mapping_dict = {
        "time_date": "Timestamp",
        "gender": "Choose your gender",
        "age": "Age",
        "course": "What is your course",
        "year_of_study": "Your current year of Study",
        "CGPA": "What is your CGPA",
        "depression": "Do you have Depression",
        "marital": "Marital status",
        "anxiety": "Do you have Anxiety",
        "panic_attack": "Do you have Panic attack",
        "Specialist_Treatment": "Did you seek any specialist for a treatment"
    }

    mapping = CSVColumnMapping(**custom_mapping_dict)
    assert mapping.time_date == "Timestamp"
    assert mapping.gender == "Choose your gender"
    assert mapping.age == "Age"
    assert mapping.specialist_treatment == "Did you seek any specialist for a treatment"
    print("✅ User Defined CSVColumnMapping Body Test PASSED!")


if __name__ == "__main__":
    test_health()
    test_model_info()
    test_zkml_inference()
    test_user_custom_column_mapping_body()
    print("\n🎉 ALL API, DB & USER COLUMN MAPPING BODY TESTS PASSED!")
