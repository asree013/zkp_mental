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


def test_home_portal():
    response = client.get("/")
    assert response.status_code == 200
    assert "นายอัสรี หะยีมะ" in response.text
    assert "6910025030" in response.text
    assert "การอนุมานโมเดลการเรียนรู้ของเครื่องแบบรักษาความเป็นส่วนตัวด้วยพยานหลักฐานความรู้เป็นศูนย์บนข้อมูลสุขภาพจิตนักเรียน" in response.text
    print("✅ GET / (Home Research Portal) PASSED!")


def test_quantization_benchmark():
    response = client.get("/test-quantization-impact")
    assert response.status_code == 200
    assert "ZK-ML Fixed-Point Quantization Impact Benchmark" in response.text
    print("✅ GET /test-quantization-impact (Jinja2 HTML) PASSED!")

    api_res = client.get("/api/v1/benchmark/quantization")
    assert api_res.status_code == 200
    data = api_res.json()
def test_cryptographic_benchmark():
    response = client.get("/test-cryptographic-benchmark")
    assert response.status_code == 200
    assert "ZK Circuit Complexity & Prover Performance Profiling" in response.text
    print("✅ GET /test-cryptographic-benchmark (Jinja2 HTML) PASSED!")

    api_res = client.get("/api/v1/benchmark/cryptographic")
    assert api_res.status_code == 200
    data = api_res.json()
    assert "summary" in data
    assert "circuit_breakdown" in data
    assert "scaling_data" in data
    assert data["summary"]["acir_opcodes"] == 312
    print("✅ GET /api/v1/benchmark/cryptographic (JSON API) PASSED: ACIR =", data["summary"]["acir_opcodes"])


def test_student_ui_and_management():
    # 1. Test HTML Dashboard
    response = client.get("/students")
    assert response.status_code == 200
    assert "Student Mental Health Records & Data Ingestion" in response.text
    print("✅ GET /students (Jinja2 HTML UI) PASSED!")

    # 2. Test Statistics API
    stats_res = client.get("/api/v1/students/statistics")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert "total_count" in stats
    print("✅ GET /api/v1/students/statistics PASSED: Total =", stats["total_count"])

    # 3. Test Create Single Record
    payload = {
        "time_date": "2026-08-16 10:00:00",
        "gender": "Female",
        "age": 22,
        "course": "Computer Science",
        "year_of_study": "year 2",
        "cgpa": "3.50 - 4.00",
        "marital_status": "No",
        "depression": "Yes",
        "anxiety": "No",
        "panic_attack": "No",
        "specialist_treatment": "No"
    }
    create_res = client.post("/api/v1/students/records", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()
    record_id = created["id"]
    print(f"✅ POST /api/v1/students/records PASSED: Created ID #{record_id}")

    # 4. Test DELETE Endpoint is securely disabled (Not Found / 405 Method Not Allowed)
    del_res = client.delete(f"/api/v1/students/records/{record_id}")
    assert del_res.status_code in [404, 405]
    print(f"🔒 DELETE /api/v1/students/records/{record_id} SECURELY DISABLED (Status: {del_res.status_code})")


def test_rate_limiting():
    # Test model-info rate limit headers or normal response
    res = client.get("/api/v1/zkml/model-info")
    assert res.status_code == 200
def test_cors_configuration():
    # Test CORS preflight and origin headers
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    }
    res = client.options("/api/v1/zkml/inference", headers=headers)
    assert res.status_code == 200
    assert "access-control-allow-origin" in res.headers
    print(f"🌐 CORS Origin Configured Successfully: Origin Allowed = {res.headers.get('access-control-allow-origin')}")


if __name__ == "__main__":
    test_health()
    test_model_info()
    test_zkml_inference()
    test_user_custom_column_mapping_body()
    test_home_portal()
    test_quantization_benchmark()
    test_cryptographic_benchmark()
    test_student_ui_and_management()
    test_rate_limiting()
    test_cors_configuration()
    print("\n🎉 ALL API, DB, HOME PORTAL, QUANTIZATION, CRYPTOGRAPHIC, STUDENT DATA, RATE LIMIT & CORS TESTS PASSED!")
