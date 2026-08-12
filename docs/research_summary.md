# 📑 รายงานสรุปงานวิจัยและสถาปัตยกรรมระบบ (Research & Architecture Summary)
## REST API สำหรับการประมวลผล ZK-ML บนข้อมูลสุขภาพจิตนักเรียน
## Development of a REST API System for ZK-ML Inference on Student Mental Health Data

---

## 📌 1. ภาพรวมและขอบเขตงานวิจัย (Research Overview & Objectives)

**เป้าหมายหลัก:**
พัฒนาระบบ RESTful API สำหรับประมวลผลโมเดล Machine Learning แบบรักษาความเป็นส่วนตัว **(Zero-Knowledge Machine Learning: ZK-ML)** บนข้อมูลสุขภาพจิตของนักเรียน โดยใช้ **Zero-Knowledge Proofs (ZKP)** ร่วมกับภาษา **Noir (Nargo DSL)** และ **FastAPI Framework**

**โจทย์วิจัยสำคัญ (Research Problem):**
การประเมินสภาวะสุขภาพจิต (ซึมเศร้า, วิตกกังวล, แพนิค) หรือการอนุมัติสวัสดิการช่วยเหลือ ปกติแล้วผู้ขอสิทธิจะต้องเปิดเผยข้อมูลสุขภาพจิตดิบซึ่งเป็น **ข้อมูลส่วนบุคคลที่อ่อนไหวสูง (Sensitive Mental Health Data)** ให้แก่ระบบหรือบุคคลภายนอก 

**แนวทางแก้ไขด้วย ZK-ML:**
นักเรียนส่งเฉพาะ **Zero-Knowledge Proof (หลักฐานเชิงคณิตศาสตร์)** ที่พิสูจน์ว่า *"ตนเองผ่านเกณฑ์การประเมินความเสี่ยงสุขภาพจิตตามโมเดล ML"* โดยที่ **ไม่มีใครรวมถึงระบบเซิร์ฟเวอร์สามารถมองเห็นข้อมูลสุขภาพจิตดิบของนักเรียนได้เลย**

---

## 🛠️ 2. สถาปัตยกรรมระบบ (MVC Architecture Overview)

ระบบได้รับการจัดโครงสร้างตามหลัก **Model-View-Controller (MVC)** เพื่อความสะอาดของโค้ด และง่ายต่อการอ้างอิงในเล่มวิจัย:

```text
zkp_mental/
├── app/                        # Core Application Package
│   ├── models/                 # [MODEL] Schemas (schemas.py) & ML Quantization (ml_model.py)
│   ├── services/               # [SERVICE] ZK Prover & Nargo Execution Engine (zk_service.py)
│   └── controllers/            # [CONTROLLER] API Handlers (health_controller.py, zkml_controller.py)
├── lib/                        # Executable CLI Helper Tools
│   ├── train_ml_model.py       # สคริปต์รันเทรน ML โมเดลและทำ Quantization
│   └── run_zkp.py              # สคริปต์รันทดสอบ ZK-ML Inference CLI
├── circuit/                    # [ZKP CIRCUIT] Noir DSL Code
│   ├── Nargo.toml              # Noir Package Configuration
│   ├── Prover.toml             # Circuit Inputs (Private & Public)
│   └── src/
│       └── main.nr             # Noir Circuit Logic for ZK-ML
├── main.py                     # FastAPI Application Entry point
├── test_api.py                 # API Integration Test Suite
├── model_weights.json          # Quantized ML Model Parameters
├── student_mental_health.csv   # Kaggle Dataset
├── requirements.txt            # Python Dependencies
└── readme.txt                  # Setup & Execution Guide
```

---

## ⚙️ 3. สรุปทางเทคนิคและการแปลงคณิตศาสตร์ (Technical & ZK-ML Details)

### 3.1 Dataset & Feature Preprocessing (`student_mental_health.csv`)
คุณลักษณะที่ใช้ฝึกสอนโมเดล ML (6 Features):
1. `Age`: อายุ (18 - 24 ปี)
2. `CGPA`: เกรดเฉลี่ย (แปลงช่วงข้อความ เช่น '3.50 - 4.00' $\rightarrow$ Integer Scaled Value $375$)
3. `Depression`: ภาวะซึมเศร้า (Binary 0 / 1)
4. `Anxiety`: ภาวะวิตกกังวล (Binary 0 / 1)
5. `Panic_Attack`: ภาวะแพนิค (Binary 0 / 1)
6. `Seek_Treatment`: การเคยพบผู้เชี่ยวชาญ (Binary 0 / 1)

### 3.2 Fixed-Point Integer Quantization Strategy
เนี่องจาก ZK Circuit (Noir DSL) ประมวลผลบน **Finite Field ($i32$ / Unsigned Integer)** ไม่สามารถประมวลผล Floating-point 64-bit โดยตรงได้ จึงใช้เทคนิค **Multiplier Quantization ($S = 10^3$)**:

$$\text{Weight}_{\text{quantized}} = \text{round}(\text{Weight}_{\text{raw}} \times 1000)$$
$$\text{Bias}_{\text{quantized}} = \text{round}(\text{Bias}_{\text{raw}} \times 1000)$$

### 3.3 Noir ZK Circuit Inference (`circuit/src/main.nr`)
- **Private Inputs (ความลับนักเรียน):** `age`, `cgpa_scaled`, `depression`, `anxiety`, `panic_attack`, `seek_treatment`
- **Public Inputs (โมเดลกลาง):** `weights: pub [i32; 6]`, `bias: pub i32`, `threshold: pub i32`, `expected_risk_class: pub u8`

**การคำนวณภายในวงจร ZK:**
$$Z = \sum_{i=1}^6 (W_i \times X_i) + B$$
$$\text{Risk\_Class} = (Z \ge \text{Threshold})$$
$$\text{assert}(\text{Risk\_Class} == \text{expected\_risk\_class})$$

---

## 📊 4. สรุปผลการทดลอง (Experimental & Benchmark Results)

| Metric / Parameter | Value / Result |
|---|---|
| **ML Model Type** | Quantized Logistic Regression Classifier |
| **Model Accuracy** | 100.00% (บน Dataset ตัวอย่าง 101 ราย) |
| **Quantized Weights** | `[-8, 2, 2552, 2716, 2749, 87]` |
| **Quantized Bias** | `-1920` |
| **ZK Proving Latency** | **~170 - 220 ms** (มิลลิวินาที) |
| **Privacy Protection** | 100% (ไม่มีการส่ง Raw Health Attributes ใน API Response) |

---

## 🌐 5. REST API Specifications

1. `GET /health` : ตรวจสอบสถานะ Nargo CLI และความพร้อมของ API Server
2. `GET /api/v1/zkml/model-info` : ดูพารามิเตอร์โมเดล ML (Weights, Bias, Scaling Factor, Accuracy)
3. `POST /api/v1/zkml/inference` : ส่งข้อมูลนักเรียนเพื่อประมวลผล ZK-ML และรับ Proof ผลการประเมิน
4. `GET /get-zpk` : สุ่มดึงตัวอย่างจาก CSV มาสคริปต์รัน ZK Proof

---

## 🤖 6. Prompts สำหรับนำไปถามต่อใน Gemini (Prompt Templates for Further Study)

คุณสามารถก๊อปปี้บทสรุปในเอกสารนี้ ร่วมกับ Prompt ด้านล่างนี้ไปวางใน Gemini บนเว็บเพื่อศึกษาต่อในหัวข้อระดับสูงได้เลยครับ:

### 💬 Prompt 1: สอบถามเกี่ยวกับการเขียนเนื้อหาเล่มวิจัย (Thesis Chapter Writing)
> *"ฉันกำลังทำวิจัยเรื่อง 'REST API สำหรับการประมวลผล ZK-ML บนข้อมูลสุขภาพจิตนักเรียน' โดยใช้ Noir DSL และ FastAPI นี่คือโครงสร้างและผลการทดลองของโปรเจกต์ฉัน [วางเนื้อหาเอกสารนี้] ช่วยเขียนยกร่างเนื้อหาบทที่ 3 (ระเบียบวิธีวิจัย / Methodology) และบทที่ 4 (ผลการทดลอง / Results) ให้หน่อย"*

### 💬 Prompt 2: ศึกษาการขยายโมเดลเป็น Neural Network / Decision Tree ใน ZK-ML
> *"อ้างอิงจากงานวิจัย ZK-ML ข้อมูลสุขภาพจิตนักเรียน [วางเนื้อหาเอกสารนี้] ตอนนี้ฉันใช้ Logistic Regression อยู่ หากฉันต้องการขยายวงจร Noir (`.nr`) ให้รองรับ Decision Tree หรือ Neural Network 2 ชั้น จะต้องปรับคณิตศาสตร์และ Quantization อย่างไรบ้าง"*

### 💬 Prompt 3: ศึกษาการปรับแต่งประสิทธิภาพและ Client-Side Proving (WebAssembly)
> *"ในงานวิจัย ZK-ML นี้ [วางเนื้อหาเอกสารนี้] ตอนนี้ Prover รันอยู่บนเซิร์ฟเวอร์ FastAPI หากฉันต้องการย้ายขั้นตอนสร้าง ZK Proof ไปรันฝั่ง Client (เช่น บน Browser ด้วย WebAssembly / Noir JS) เพื่อให้เป็น True Client-Side Privacy จะต้องวางสถาปัตยกรรมอย่างไร"*
