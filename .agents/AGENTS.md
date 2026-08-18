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

### ⚡ 3.2 Cryptographic & Circuit Performance Profile (ผลการทดลองด้านรหัสวิทยา)

| Metric / Dimension | Value | Unit | Research Significance & Chapter 4 Insight |
|---|:---:|:---:|---|
| **ACIR Circuit Constraints** | **312** | Opcodes | วงจร Noir Circuit (`main.nr`) มีขนาดกะทัดรัด (Ultra-Lightweight) |
| **Brillig Opcodes** | **17** | Opcodes | ฟังก์ชันคำนวณนอก Constraint (Unconstrained Quotient / Invert) |
| **Mean Proving Latency** | **~185.4** | ms | เวลาเฉลี่ยสร้าง Witness & Proof บน Single Core CPU |
| **95th Percentile Latency (P95)** | **~210.2** | ms | ความเสถียรของระบบภายใต้โหลด (Jitter $\le \pm 25$ ms) |
| **Theoretical Throughput** | **~5.4** | Req/sec | Single Worker Throughput (ขยายได้ด้วย Multi-process Workers) |
| **Feature Scaling Complexity** | **$O(N)$** | Linear | Constraints เติบโตเชิงเส้น: $120 + 32 \times N$ opcodes |

---

### 🧠 3.3 Model Selection Rationale: Why Logistic Regression over Decision Tree, Naive Bayes, & Random Forest? (เหตุผลเชิงวิชาการในการเลือกโมเดลสำหรับ ZK-ML)

| มิติการเปรียบเทียบ | Logistic Regression ⭐ (งานวิจัยนี้) | Decision Tree / Random Forest | Naive Bayes |
|---|:---:|:---:|:---:|
| **รูปแบบการคำนวณใน ZK Circuit** | **Linear Combination (คูณและบวก)** | Conditional Branching (`if/else` หลายชั้น) | Probability Product / Log-Likelihood ($\log P$) |
| **ขนาด Circuit Constraints** | **312 Constraints** (Ultra-Lightweight) | 5,000 - 50,000+ Constraints (ขนาดใหญ่มาก) | 3,000 - 10,000+ Constraints |
| **เวลาสร้าง Proof (Proving Time)** | **~185.4 ms (Sub-second)** | 1.5 - 10+ วินาที | 1.2 - 4 วินาที |
| **ความเสี่ยงข้อมูลรั่วไหล (Side-channel/Leakage)** | **ไม่มี** (คำนวณสมการเดียวแบบคงที่) | เสี่ยง Branch Leakage (ต้องคำนวณทุกกิ่งในป่า) | ความคลาดเคลื่อนจากการประมาณค่าทศนิยม |
| **ความซับซ้อนของการ Quantize** | **ง่ายและแม่นยำ 100% ($S=1,000$)** | ต้อง Quantize ทุก Threshold ในแต่ละ Node | ต้อง Quantize ค่า Probability และ Logarithm |

#### 💡 ประเด็นอภิปรายและข้อต่อสู้เชิงวิชาการ (Scientific & Cryptographic Justification):
1. **ปัญหาของ Decision Tree / Random Forest ใน ZK Circuit (Branching Overhead):**
   - ในระบบปกติ `if (age > 20)` จะกระโดดข้ามไปกิ่งที่ต้องการได้อย่างรวดเร็ว แต่ใน **Zero-Knowledge Proofs (Noir / R1CS Finite Field)** เพื่อไม่ให้ผู้ตรวจสอบรู้ว่าข้อมูลของนักเรียนตกอยู่ที่กิ่งไหน (Privacy Preservation) วงจร ZK จำเป็นต้องคำนวณทุกกิ่งของทุกต้นไม้ (Evaluate All Branches via Multiplexers)
   - การใช้ Random Forest (50-100 ต้นไม้) จะทำให้ขนาดวงจรพุ่งสูงเป็น **หลายหมื่น Opcodes** ส่งผลให้ Proving Latency ช้าลงหลายเท่าตัว เปลือง RAM มหาศาล และไม่เหมาะกับการประมวลผลบน Client/Web
2. **ปัญหาของ Naive Bayes ใน ZK Circuit (Non-linear & Logarithm Complexity):**
   - Naive Bayes ต้องคำนวณผลคูณความน่าจะเป็น $P(x_1|y) \times P(x_2|y) \times ...$ หรือใช้ $\sum \log P(x_i|y)$
   - ใน ZK Finite Field ไม่มีฟังก์ชัน $\log$ หรือเลขทศนิยมโดยตรง การประมาณค่า $\log$ และการหาร (Division) ต้องใช้ Brillig Opcodes หรือ Polynomial Approximation ซึ่งสร้าง Rounding Errors สูงและสิ้นเปลือง Constraints
3. **เหตุผลที่ Logistic Regression คือจุดเหมาะสมที่สุด (Optimal Trade-off):**
   - **Linear Compatibility**: แปลงเป็นสมการผลรวมเชิงเส้น $\sum (w_i \times x_i) + b \ge 0$ มีเฉพาะการคูณและบวกเลขจำนวนเต็ม (`i32`) บน Finite Field ได้ตรงไปตรงมา
   - **No Accuracy Trade-off**: ชุดข้อมูลสุขภาพจิตนักเรียนมี Feature สำคัญ (Depression, Anxiety, Panic) ที่สามารถแบ่งแยกกลุ่มเสี่ยง (Linearly Separable) ได้สมบูรณ์แบบที่ความแม่นยำ $100\%$ อยู่แล้ว การใช้โมเดลที่ซับซ้อนกว่านี้จึงเป็น Overkill โดยไม่เพิ่มความแม่นยำ แต่เพิ่ม Cryptographic Overhead มหาศาล
   - **High Real-Time Throughput**: ใช้วงจรเพียง 312 Constraints สร้าง Proof ได้เร็วเพียง ~185 ms ตอบสนองได้ทันทีตามมาตรฐานความปลอดภัย PDPA

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

### Rule 4: Standardized Education Level Enum Specification (รหัสย่อระดับการศึกษา)
ฟิลด์ `education_level` ในฐานข้อมูลและ API ใช้รหัสย่อ Enum มาตรฐาน หากไม่มีการระบุหรือไม่กรอกข้อมูล ระบบจะกำหนดค่าเริ่มต้นเป็น `UNK` เสมอ:

| Code (ตัวย่อ) | Full Name / Description | ภาษาไทย | หมายเหตุ / ตัวอย่าง |
|:---:|---|---|---|
| **`PP`** | Pre-primary Education | การศึกษาก่อนประถมศึกษา | อนุบาล / ก่อนวัยเรียน |
| **`PE`** | Primary Education | ประถมศึกษา | ป.1 - ป.6 |
| **`LSE`** | Lower Secondary Education | มัธยมศึกษาตอนต้น | ม.1 - ม.3 |
| **`USE_VS`** | Upper Secondary Education / Vocational Stream | มัธยมศึกษาตอนปลาย / สายอาชีวศึกษา | ม.4 - ม.6, ปวช. |
| **`BBDL`** | Below bachelor's degree level | ต่ำกว่าปริญญาตรี | อนุปริญญา, ปวส. |
| **`BD`** | Bachelor's degree | ปริญญาตรี | ป.ตรี / Undergraduate |
| **`MD`** | Master's Degree | ปริญญาโท | ป.โท / Postgraduate |
| **`PHD`** | Doctoral Degree | ปริญญาเอก | ป.เอก / Doctorate |
| **`UNK`** | Unknown / Not Specified | ไม่ทราบ / ไม่ได้ระบุ | **Default (ค่าเริ่มต้นเมื่อไม่กรอกข้อมูล)** |

---

## 🌐 5. Standardized Endpoints Specification

| Method | Endpoint | Description | Return Type |
|---|---|---|---|
| `GET` | `/` | Master's Thesis Research Portal Home Page | HTML (Jinja2) |
| `GET` | `/students` | Student Mental Health Data & CSV Ingestion Dashboard | HTML (Jinja2) |
| `GET` | `/test-quantization-impact` | Interactive Quantization Benchmark Dashboard | HTML (Jinja2) |
| `GET` | `/test-cryptographic-benchmark` | ZK Cryptographic & Circuit Performance Dashboard | HTML (Jinja2) |
| `GET` | `/health` | Health check, DB connection & Nargo CLI status | JSON |
| `GET` | `/api/v1/zkml/model-info` | Public Quantized Weights & Model Metadata | JSON |
| `POST` | `/api/v1/zkml/inference` | ZK-ML Private Inference & Proof Verification | JSON |
| `GET` | `/api/v1/students/records` | List of Student Mental Health DB Records | JSON |
| `POST` | `/api/v1/students/records` | Create Single Student Mental Health Record | JSON |
| `POST` | `/api/v1/students/upload-csv` | Upload & Ingest CSV File to MySQL Database | JSON |
| `GET` | `/api/v1/students/statistics` | Student Risk & Mental Health Statistics | JSON |
| `GET` | `/paper` | Research Papers & PDF Repository Web Dashboard | HTML (Jinja2) |
| `POST` | `/api/upload/pdf` | Upload PDF Research Paper to `./uploads` with Timestamp Link | JSON |
| `POST` | `/api/v1/papers/upload` | Upload PDF Research Paper (v1 Alias) | JSON |
| `GET` | `/api/v1/papers/records` | List All Uploaded Research Papers from DB | JSON |
| `GET` | `/api/v1/papers/records/{id}` | Get Specific Research Paper by ID | JSON |
| `PUT` | `/api/v1/papers/records/{id}` | Update Research Paper Name & Type | JSON |
| `DELETE` | `/api/v1/papers/records/{id}` | Delete Research Paper (Requires `pass_for_delete=P@ssw0rd`) | JSON |
| `GET` | `/api/v1/benchmark/quantization` | Raw Quantization Benchmark Dataset & MAE | JSON |
| `GET` | `/api/v1/benchmark/cryptographic` | ZK Circuit Constraints & Latency Profile | JSON |


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
