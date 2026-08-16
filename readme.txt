# ZK-ML Student Mental Health Research Project Setup Guide

## Prerequisites & Installation

โปรเจกต์นี้ใช้ Zero-Knowledge Proofs (ZKP) ผ่านทาง Noir (Nargo CLI) คู่กับ FastAPI Framework (Python 3.10+)

### 1. ติดตั้ง Nargo (Noir CLI)
- **สำหรับ macOS / Linux:**
  curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash
  source ~/.zshrc  # หรือ ~/.bashrc
  noirup

---

## How to Run Project

### 1. สร้างและเรียกใช้ Virtual Environment
python3 -m venv venv
source venv/bin/activate

### 2. ติดตั้ง Python Libraries
pip install -r requirements.txt

### 3. รันการเทรนและ Quantize โมเดล ML (Optional)
python lib/train_ml_model.py

### 4. รันคำสั่งทดสอบ ZK-ML Inference CLI
python lib/run_zkp.py 2

### 5. รันเซิร์ฟเวอร์ FastAPI REST API
python main.py
# หรือ uvicorn main:app --reload --host 0.0.0.0 --port 8000

### 6. การทดสอบและดูผลการทดลองวิจัย ป.โท (Thesis Benchmarks)
- **Research Portal Homepage**: เข้าเบราว์เซอร์ไปที่ `http://localhost:8000/`
- **1) Quantization Impact Dashboard (Jinja2)**: `http://localhost:8000/test-quantization-impact`
- **2) Cryptographic & ZK Benchmark (Jinja2)**: `http://localhost:8000/test-cryptographic-benchmark`
- **JSON REST API Endpoints**: 
  - `http://localhost:8000/api/v1/benchmark/quantization`
  - `http://localhost:8000/api/v1/benchmark/cryptographic`
- **CLI Benchmark Scripts**: 
  - `python lib/benchmark_quantization.py`
  - `python lib/benchmark_zk_performance.py`
*(ระบบใช้ Hybrid Data Provider: ดึงข้อมูลจาก MySQL DB เป็นอันดับแรก พร้อม Fallback ไป CSV อัตโนมัติ)*

### 7. การ Deploy ด้วย Docker & Docker Compose (Container Deployment)
```bash
# รันทั้งระบบ (FastAPI + Noir CLI + MySQL) ด้วยคำสั่งเดียว
docker compose up -d --build

# ดูสถานะและ Logs
docker compose ps
docker compose logs -f api

# ปิดระบบ
docker compose down
```

---

## Project Structure
- `app/models/` : Data Schemas, DB Models & Hybrid ML Data Loader
- `app/services/` : ZK Prover & Benchmark Engine
- `app/controllers/` : API Route Controllers & Jinja2 Template View
- `app/templates/` : Jinja2 HTML Templates (Quantization Impact UI)
- `lib/` : Runnable CLI Scripts (`train_ml_model.py`, `run_zkp.py`, `benchmark_quantization.py`)
- `circuit/` : Noir ZK DSL Circuit (`src/main.nr`)
- `main.py` : FastAPI Server Entry point

## Dataset Info
- **File**: `student_mental_health.csv`
- **Database Table**: `mental_health_records` (MySQL)
- **Description**: แบบสำรวจสภาวะสุขภาพจิตของนักเรียน (Student Mental Health Survey Dataset)
- **Source**: Kaggle Dataset