# ZKP Mental Health Project Setup

## Prerequisites
โปรเจกต์นี้ใช้ Zero-Knowledge Proofs (ZKP) ผ่านทาง Noir (Nargo) คู่กับ FastAPI (Python) ดังนั้นผู้ใช้งานจำเป็นต้องติดตั้งเครื่องมือต่อไปนี้:

### 1. ติดตั้ง Nargo (Noir CLI)
เนื่องจากระบบมีการรันคำสั่ง Noir ในเบื้องหลัง เครื่องคอมพิวเตอร์ที่รันโปรเจกต์นี้จำเป็นต้องติดตั้ง Nargo:

- **สำหรับ macOS / Linux:**
  รันคำสั่งต่อไปนี้ใน Terminal เพื่อติดตั้ง `noirup` และ `nargo`:
  
  curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash
  # จากนั้นปิดหน้าจอ Terminal แล้วเปิดใหม่ หรือรันคำสั่ง:
  source ~/.bashrc # หรือ ~/.zshrc แล้วแต่ shell ที่ใช้
  # ติดตั้งเวอร์ชันล่าสุดด้วยการรัน:
  noirup
 
  *(สำหรับ Windows แนะนำให้อ่านคู่มือเพิ่มเติมที่ https://noir-lang.org/docs/getting_started/installation/)*

---

## How to Run Project

### 1. สร้างและเรียกใช้ Virtual Environment
python3 -m venv venv
source venv/bin/activate


### 2. ติดตั้ง Python Libraries
pip install -r requirements.txt


### 3. รันเซิร์ฟเวอร์ FastAPI
uvicorn main:app --reload
# หรือล็อก IP และ Port
uvicorn main:app --reload --host 0.0.0.0 --port 8000

##ข้อมูลที่ใช้
ข้อมูลจากไฟล์ : student_mental_health.csv
description : เป็นแบบสำรวจสุขภาพจิตของนักเรียน
ที่มา : https://www.kaggle.com/code/melikedilekci/student-mental-health/input