# AGENTS.md - Master's Thesis Research Guidelines & Knowledge Base

# การอนุมานโมเดลการเรียนรู้ของเครื่องแบบรักษาความเป็นส่วนตัวด้วยพยานหลักฐานความรู้เป็นศูนย์บนข้อมูลสุขภาพจิตนักเรียน
# Privacy-Preserving Machine Learning Inference Using Zero-Knowledge Proofs on Student Mental Health Data

---

## 📌 1. Executive Summary & Research Scope (ขอบเขตงานวิจัย ป.โท)

งานวิจัยนี้เป็นวิทยานิพนธ์ระดับปริญญาโท (วิทยาศาสตรมหาบัณฑิต สาขาวิทยาการข้อมูล - M.Sc. in Data Science แผน ก แบบ ก 2)
มุ่งเน้นการแก้ปัญหา **ความเป็นส่วนตัวของข้อมูลสุขภาพจิตนักเรียน (Sensitive Mental Health Data Privacy & PDPA Compliance)** 
โดยพัฒนาระบบ **Privacy-Preserving Machine Learning (PPML) Inference** ผ่านเทคโนโลยี **Zero-Knowledge Proofs (ZKP)** ร่วมกับภาษา **Noir DSL (Nargo)**, **Integer Fixed-Point Quantization**, และ **FastAPI Framework (MVC Architecture)** พร้อมหน้าวิเคราะห์ผลการทดลองด้วย **Jinja2 Web Dashboard**

---

## 🛠️ 2. Core Tech Stack & System Architecture

| Layer | Technology / Tool | Role / Description |
|---|---|---|
| **Privacy / ZKP** | Noir DSL (`.nr`), Nargo CLI | เขียน ZK Circuit สำหรับ Private ML Inference & Constraint Verification |
| **Machine Learning** | Scikit-learn, NumPy, Pandas | Logistic Regression (Linear Classifier), Quantization & Scaling Engine |
| **Backend & Web API** | Python 3.10+, FastAPI, Uvicorn | High-performance Asynchronous RESTful API (MVC Pattern) |
| **Web Visualization** | Jinja2 Templates, Chart.js | Interactive Benchmark Web Dashboard (`/test-quantization-impact`) |
| **Database & Storage** | MySQL, SQLAlchemy ORM | ตาราง `mental_health_records` รองรับ Hybrid Data Provider (DB + Fallback CSV) |
| **Data Validation** | Pydantic v2 | ตรวจสอบ Schema ของ Request, Response และ ZK Metadata |

---

## 🔬 3. Empirical Research Findings: Quantization Impact Benchmark (ผลการทดลองสำคัญสำหรับทำ Paper/Thesis)

### 📊 ตารางผลการทดลองจริง (Benchmark Results Table)

| Representation & Method | Scaling Factor ($S$) | Accuracy (%) | Precision | Recall | F1-Score | $\Delta\text{Acc}$ (%) | Mismatches | Score Drift (MAE) | Status / Evaluation |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Baseline (Float64)** | - | **100.0%** | **1.0000** | **1.0000** | **1.0000** | 0.0% | 0 | 0.000000 | Reference Baseline |
| **Quantized (S=1)** | 1 | 63.41% | 0.6341 | 1.0000 | 0.7761 | -36.59% | 15 | 1.361642 | ❌ Loss (15 Mismatches) |
| **Quantized (S=5)** | 5 | 65.85% | 1.0000 | 0.4615 | 0.6316 | -34.15% | 14 | 2.370065 | ❌ Loss (14 Mismatches) |
| **Quantized (S=10)** | 10 | 100.0% | 1.0000 | 1.0000 | 1.0000 | 0.0% | 0 | 0.360309 |  Optimal (No Loss) |
| **Quantized (S=50)** | 50 | 100.0% | 1.0000 | 1.0000 | 1.0000 | 0.0% | 0 | 0.382748 |  Optimal (No Loss) |
| **Quantized (S=100)** | 100 | 100.0% | 1.0000 | 1.0000 | 1.0000 | 0.0% | 0 | 0.370065 |  Optimal (No Loss) |
| **Quantized (S=500)** | 500 | 100.0% | 1.0000 | 1.0000 | 1.0000 | 0.0% | 0 | 0.246764 |  Optimal (No Loss) |
| **Quantized (S=1000)** | **1,000** | **100.0%** | **1.0000** | **1.0000** | **1.0000** | **0.0%** | **0** | **0.082382** | ⭐ **Selected in ZK Circuit** |
| **Quantized (S=5000)** | 5,000 | 100.0% | 1.0000 | 1.0000 | 1.0000 | 0.0% | 0 | 0.024724 |  Optimal (No Loss) |
| **Quantized (S=10000)** | 10,000 | 100.0% | 1.0000 | 1.0000 | 1.0000 | 0.0% | 0 | 0.008332 |  Optimal (No Loss) |
| **Quantized (S=100000)**| 100,000 | 100.0% | 1.0000 | 1.0000 | 1.0000 | 0.0% | 0 | 0.001188 |  Optimal (Risk of Overflow) |

---

### 💡 การอภิปรายผลเชิงวิชาการ (Scientific Discussion Points for Chapter 4):
1. **สาเหตุความล้มเหลวที่ $S=1, 5$ (Information Annihilation & Weight Distortion):**
   - น้ำหนักของ `Age` ($-0.0481$) และ `CGPA` ($+0.0015$) มีขนาดเล็ก เมื่อคูณ $S=1$ แล้วปัดเศษ จะถูกปัดทิ้งกลายเป็น $0$ ทำให้โมเดลตัด Feature สำคัญทิ้งไป
   - อัตราส่วนระหว่าง Bias และ Feature Weights เสียสมดุล ส่งผลให้ Score รวมคำนวณข้ามฝั่ง Threshold ผิด เกิด Mismatch สูงถึง 14-15 ตัวอย่าง
2. **เหตุผลที่เลือกใช้ $S=1,000$ (Optimal Trade-off Point):**
   - ให้ความแม่นยำ $100\%$ สมบูรณ์ ($\Delta\text{Accuracy} = 0.0\%$, Mismatches = 0)
   - ค่าความคลาดเคลื่อนของคะแนน (Score Drift MAE) ต่ำมากเพียง $0.0823$
   - ขนาดผลคูณของตัวเลขยังอยู่ในช่วงของชนิดข้อมูล `i32` ใน Noir Finite Field ไม่เสี่ยงต่อปัญหา Integer Overflow เหมือนสเกล $S \ge 100,000$

---

## 🎯 4. AI Development Directives & Zero-Knowledge Security Rules

### Rule 1: Zero-Knowledge Privacy Standard (ห้ามรั่วไหลข้อมูลส่วนบุคคล)
1. **Private Inputs Only**: ข้อมูลสุขภาพจิต (`age`, `cgpa_scaled`, `depression`, `anxiety`, `panic_attack`, `seek_treatment`) ต้องเป็น Private Variables ใน `circuit/src/main.nr` ห้ามใส่คีย์เวิร์ด `pub`
2. **Public Parameters**: เฉพาะพารามิเตอร์โมเดลมาตรฐานสาธารณะ (`pub weights`, `pub bias`, `pub threshold`, `pub expected_risk_class`) เท่านั้นที่เป็น `pub`
3. **No Raw Leakage in API**: REST API ต้องตอบกลับเฉพาะ Verification Status (`Pass`/`Not Pass`), Risk Label, Proving Time และ Proof Metadata เท่านั้น

### Rule 2: Hybrid Data Provider Pattern (สถาปัตยกรรมข้อมูลแบบไฮบริด)
- ฟังก์ชัน `load_dataset_hybrid()` ใน `app/models/ml_model.py` จะพยายามอ่านข้อมูลจาก **MySQL Database (`mental_health_records`) เป็นอันดับแรก**
- หากฐานข้อมูลว่างเปล่าหรือไม่ได้เชื่อมต่อ จะ **Fallback ไปอ่านจาก `student_mental_health.csv` ให้อัตโนมัติ**

### Rule 3: Asynchronous REST API Standards
- คำสั่ง Nargo CLI (`nargo execute`, `nargo prove`) ต้องสั่งผ่าน `asyncio.create_subprocess_exec` เสมอ เพื่อไม่บล็อก Main Event Loop

---

## 🌐 5. Standardized Endpoints Specification

| Method | Endpoint | Description | Return Type |
|---|---|---|---|
| `GET` | `/health` | Health check, DB connection & Nargo CLI status | JSON |
| `GET` | `/api/v1/zkml/model-info` | Public Quantized Weights & Model Metadata | JSON |
| `POST` | `/api/v1/zkml/inference` | ZK-ML Private Inference & Proof Verification | JSON |
| `GET` | `/get-zpk` | ทดสอบรัน ZK Inference จากชุดข้อมูลตัวอย่าง | JSON |
| `GET` | `/test-quantization-impact` | Interactive Web Dashboard สำหรับผลการทดลองวิทยานิพนธ์ | HTML (Jinja2) |
| `GET` | `/api/v1/benchmark/quantization` | Raw Quantization Benchmark Dataset & MAE | JSON |

---

## 📁 6. Project Directory Structure

```text
zkp_mental/
├── app/                        # MVC Application Package
│   ├── config/                 # [CONFIG] Database connection (database.py)
│   ├── models/                 # [MODEL] Schemas (schemas.py), DB Models (db_models.py), ML Quantization (ml_model.py)
│   ├── services/               # [SERVICE] ZK Prover (zk_service.py), Benchmark Engine (benchmark_service.py), Student Service
│   ├── controllers/            # [CONTROLLER] API Handlers (health, zkml, student, benchmark)
│   └── templates/              # [VIEW] Jinja2 HTML Templates (quantization_impact.html)
├── circuit/                    # ZK Circuit (Noir DSL)
│   ├── Nargo.toml              # Noir package file
│   ├── Prover.toml             # Circuit inputs (Private & Public)
│   └── src/
│       └── main.nr             # Noir circuit logic for ZK-ML
├── lib/                        # Helper & Executable CLI Benchmark Tools
│   ├── train_ml_model.py       # ML Training & Quantization CLI tool
│   ├── run_zkp.py              # ZK Execution CLI testing tool
│   └── benchmark_quantization.py # CLI Quantization Benchmark Tool
├── main.py                     # FastAPI Application entry point
├── test_api.py                 # Automated Test Suite
├── student_mental_health.csv   # Baseline Student Mental Health dataset
├── requirements.txt            # Python dependencies
└── readme.txt                  # Setup & execution guide
```
