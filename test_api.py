"""
API Test Suite - Verification of MVC Architecture & ZK-ML Endpoints
"""

from fastapi.testclient import TestClient
from main import app

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


def test_sample_get():
    response = client.get("/get-zpk?count_student=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    print("✅ GET /get-zpk PASSED: Evaluated 2 sample students")


if __name__ == "__main__":
    test_health()
    test_model_info()
    test_zkml_inference()
    test_sample_get()
    print("\n🎉 ALL MVC API TESTS PASSED SUCCESSFULLY!")
