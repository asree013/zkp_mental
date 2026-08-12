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

---

## Project Structure
- `app/models/` : Data Schemas & ML Model Training / Quantization
- `app/services/` : ZK Prover & Nargo Execution Engine
- `app/controllers/` : API Route Controllers
- `lib/` : Runnable CLI Scripts (`train_ml_model.py`, `run_zkp.py`)
- `circuit/` : Noir ZK DSL Circuit (`src/main.nr`)
- `main.py` : FastAPI Server Entry point

## Dataset Info
- **File**: `student_mental_health.csv`
- **Description**: แบบสำรวจสภาวะสุขภาพจิตของนักเรียน (Student Mental Health Survey Dataset)
- **Source**: Kaggle Dataset