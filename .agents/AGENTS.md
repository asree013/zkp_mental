# AGENTS.md - AI Development Prompt & Guidelines for ZK-ML Research Project

# REST API สำหรับการประมวลผล ZK-ML บนข้อมูลสุขภาพจิตนักเรียน
# Development of a REST API System for ZK-ML Inference on Student Mental Health Data

---

## 📌 1. Executive Summary & Research Scope (ขอบเขตงานวิจัย)

โปรเจกต์นี้เป็นงานวิจัยพัฒนาระบบ **REST API สำหรับการประมวลผล Zero-Knowledge Machine Learning (ZK-ML) บนข้อมูลสุขภาพจิตนักเรียน** 
มีเป้าหมายเพื่อสร้างระบบตรวจสอบและประเมินสภาวะสุขภาพจิต (เช่น ซึมเศร้า, วิตกกังวล, แพนิค) หรือการอนุมัติสิทธิสวัสดิการ โดยที่ **ผู้ใช้งาน/นักเรียนไม่ต้องเปิดเผยข้อมูลส่วนบุคคลที่อ่อนไหว (Sensitive Mental Health Data)** แก่ระบบหรือบุคคลภายนอก ผ่านการประยุกต์ใช้ **Zero-Knowledge Proofs (ZKP)** ร่วมกับภาษา **Noir (Nargo)** และ **FastAPI Framework** ในรูปแบบสถาปัตยกรรม **MVC (Model-View-Controller)**

---

## 🛠️ 2. Core Tech Stack & Requirements

| Layer | Technology / Tool | Role / Description |
|---|---|---|
| **Backend API** | Python 3.10+, FastAPI, Uvicorn | ให้บริการ RESTful Endpoints สำหรับ ZK Inference และ Verification |
| **Architecture** | MVC / Layered Architecture | จัดกลุ่ม `app/models/`, `app/services/`, `app/controllers/` |
| **Data Validation** | Pydantic v2 | กำหนด Schemas ของ Request, Response และ ZK Payload |
| **ZKP Framework** | Noir DSL (`.nr`), Nargo CLI | เขียน ZK Circuit สำหรับตรวจสอบเงื่อนไขสุขภาพจิตและคำนวณ Proof |
| **Data Science** | Pandas, Scikit-learn, NumPy | อ่านและเตรียมข้อมูลจาก `student_mental_health.csv` |
| **Helper Libs** | `lib/train_ml_model.py`, `lib/run_zkp.py` | สคริปต์สำหรับการทดสอบรัน CLI และการเทรนโมเดล |

---

## 🎯 3. AI Assistant Core Directives & Rules (ข้อกำหนดการทำงานสำหรับ AI)

### Rule 1: Strict Zero-Knowledge Privacy Standard (หลักการรักษาความลับข้อมูล)
1. **Private Inputs Only for Sensitive Data**: ข้อมูลสุขภาพจิต เช่น `age`, `depression`, `anxiety`, `panic_attack`, `cgpa` ต้องถูกกำหนดเป็น **Private variables** ใน Noir Circuit (`src/main.nr`) ห้ามใส่คีย์เวิร์ด `pub` นำหน้าข้อมูลเหล่านี้โดยเด็ดขาด
2. **Public Input Minimization**: กำหนดตัวแปร `pub` เฉพาะค่าเกณฑ์มาตรฐานกลางและพารามิเตอร์โมเดลที่ยอมรับได้ทางสาธารณะเท่านั้น เช่น `pub weights`, `pub bias`, `pub threshold`, `pub expected_risk_class`
3. **No Sensitive Data Leakage in API Responses**: ผลลัพธ์ที่ตอบกลับผ่าน REST API ต้องส่งคืนเฉพาะสถานะ verification (`Pass`/`Not Pass`), ZK Proof payload, และ Public Metadata เท่านั้น **ห้ามส่งข้อมูล Raw Health Features กลับไปใน Response**

### Rule 2: ZK-ML & Noir Circuit Engineering Standards
1. **Fixed-Point & Integer Quantization**: Noir Circuit ไม่รองรับ Floating Point 64-bit โดยตรง AI ต้องแปลง Weights/Inputs เป็น Integer/Fixed-point Representation (Scaling Multiplier $10^3$)
2. **Safe File Handling for Prover.toml**: การสร้าง/อัปเดตไฟล์ `Prover.toml` จาก Python จะต้องใช้วิธีที่ปลอดภัย มี Validation และทำ Cleanup เสมอเพื่อป้องกัน Race Condition

### Rule 3: REST API & Backend Architecture Standards (MVC Pattern)
1. **Asynchronous Execution**: การสั่งรัน Nargo CLI (`nargo execute`, `nargo prove`, `nargo verify`) ต้องไม่ Block FastAPI Main Event Loop ใช้ `asyncio.create_subprocess_exec`
2. **Standardized REST API Endpoints**:
   - `GET /health` - Health check & Nargo status
   - `GET /api/v1/zkml/model-info` - ข้อมูล Public Weights & Quantization Metadata
   - `POST /api/v1/zkml/inference` - ส่งข้อมูลป้อนเข้า ZK Circuit เพื่อสร้าง Proof และรับผลลัพธ์
   - `GET /get-zpk` - ทดสอบรัน ZK Inference จากชุดข้อมูลตัวอย่าง

---

## 📁 4. Project Directory Structure

```text
zkp_mental/
├── app/                        # MVC Application Package
│   ├── models/                 # [MODEL] Schemas (schemas.py) & ML Quantization (ml_model.py)
│   ├── services/               # [SERVICE] ZK Prover & Nargo Execution Engine (zk_service.py)
│   └── controllers/            # [CONTROLLER] API Handlers (health_controller.py, zkml_controller.py)
├── circuit/                    # ZK Circuit (Noir)
│   ├── Nargo.toml              # Noir package file
│   ├── Prover.toml             # Circuit inputs (Private & Public)
│   └── src/
│       └── main.nr             # Noir circuit logic for ZK-ML
├── lib/                        # Helper & Executable CLI Scripts
│   ├── train_ml_model.py       # ML Training & Quantization CLI tool
│   └── run_zkp.py              # ZK Execution CLI testing tool
├── main.py                     # FastAPI Application entry point
├── test_api.py                 # API Test Suite
├── student_mental_health.csv   # Student Mental Health dataset
├── requirements.txt            # Python dependencies
└── readme.txt                  # Setup & execution guide
```
