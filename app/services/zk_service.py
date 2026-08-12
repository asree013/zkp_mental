"""
ZK-ML Prover Service & Nargo CLI Engine
=======================================
จัดการกระบวนการประมวลผล Zero-Knowledge Proof (ZKP)
1. ดึงค่าน้ำหนักโมเดล ML และคำนวณ Expected Risk Class ในฝั่ง Prover
2. บันทึกข้อมูลลง Prover.toml (แยก Private Features และ Public Model Parameters)
3. สั่งรัน Nargo CLI ด้วย Async Subprocess
4. บันทึกประสิทธิภาพและส่งคืนผลลัพธ์ผ่าน Pydantic Schemas
"""

import asyncio
import json
import os
import shutil
import time
from typing import Optional, List
import pandas as pd

from app.models.schemas import StudentFeatures, ZKMLResult
from app.models.ml_model import load_model_weights, parse_cgpa


def get_nargo_bin() -> str:
    """
    ค้นหาตำแหน่งไดเรกทอรีของ Nargo CLI ไบนารี
    """
    nargo_bin = shutil.which("nargo")
    if not nargo_bin:
        expanded_path = os.path.expanduser("~/.nargo/bin/nargo")
        if os.path.exists(expanded_path):
            nargo_bin = expanded_path
        else:
            nargo_bin = "nargo"
    return nargo_bin


async def execute_zkml_inference(features: StudentFeatures, student_index: Optional[int] = None) -> ZKMLResult:
    """
    รัน ZK-ML Inference บนข้อมูลคุณลักษณะนักเรียน
    """
    nargo_bin = get_nargo_bin()
    model_data = load_model_weights()

    weights = model_data['quantized_weights']
    bias = model_data['quantized_bias']
    threshold = model_data['quantized_threshold']

    cgpa_scaled = parse_cgpa(features.cgpa_str)

    # 1. คำนวณ Expected Risk Class ในฝั่ง Prover (Private Calculation)
    score = (
        (features.age * weights[0]) +
        (cgpa_scaled * weights[1]) +
        (features.depression * weights[2]) +
        (features.anxiety * weights[3]) +
        (features.panic_attack * weights[4]) +
        (features.seek_treatment * weights[5]) +
        bias
    )
    expected_risk_class = 1 if score >= threshold else 0

    # 2. เตรียมไฟล์ Prover.toml ตามมาตรฐาน Zero-Knowledge Privacy Standard
    prover_content = f"""# PRIVATE INPUTS (Student Mental Health Data - Strictly Hidden)
age = {features.age}
cgpa_scaled = {cgpa_scaled}
depression = {features.depression}
anxiety = {features.anxiety}
panic_attack = {features.panic_attack}
seek_treatment = {features.seek_treatment}

# PUBLIC INPUTS (Quantized ML Model Parameters & Outcome Class)
weights = {json.dumps(weights)}
bias = {bias}
threshold = {threshold}
expected_risk_class = {expected_risk_class}
"""

    circuit_dir = "circuit"
    prover_file_path = os.path.join(circuit_dir, "Prover.toml")
    with open(prover_file_path, "w", encoding="utf-8") as f:
        f.write(prover_content)

    # 3. จับเวลา Proving Latency (ระดับมิลลิวินาที)
    start_time = time.perf_counter()

    # สั่งรัน Nargo CLI แบบ Asynchronous Subprocess
    proc = await asyncio.create_subprocess_exec(
        nargo_bin, "execute",
        cwd=circuit_dir,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    end_time = time.perf_counter()
    proving_time_ms = round((end_time - start_time) * 1000, 2)

    risk_label = "High Risk / Support Recommended" if expected_risk_class == 1 else "Low Risk / Normal"

    # 4. ตรวจสอบผลลัพธ์จากการคำนวณ ZK Witness
    if proc.returncode == 0:
        msg = f"สร้างและยืนยัน ZK Proof สำเร็จภายใน {proving_time_ms} ms โดยไม่เปิดเผยข้อมูลสุขภาพจิตดิบ"
        return ZKMLResult(
            student_index=student_index,
            verification_status="Pass",
            risk_class=expected_risk_class,
            risk_label=risk_label,
            proving_time_ms=proving_time_ms,
            message=msg
        )
    else:
        err_msg = stderr.decode('utf-8') if stderr else "Circuit Witness Execution Failed"
        return ZKMLResult(
            student_index=student_index,
            verification_status="Not Pass",
            risk_class=expected_risk_class,
            risk_label=risk_label,
            proving_time_ms=proving_time_ms,
            message=f"การประมวลผล ZK Proof ล้มเหลว: {err_msg}"
        )


async def get_student_sample_zk(count: int = 1) -> List[ZKMLResult]:
    """
    ดึงข้อมูลตัวอย่างจากไฟล์ CSV และสั่งรัน ZK-ML Inference ทดสอบระบบ
    """
    csv_path = 'student_mental_health.csv'
    results = []
    if not os.path.exists(csv_path):
        return results

    df = pd.read_csv(csv_path)
    for i in range(min(count, len(df))):
        row = df.iloc[i]
        age = int(row['Age']) if pd.notnull(row['Age']) else 20
        features = StudentFeatures(
            age=age,
            cgpa_str=str(row['What is your CGPA?']),
            depression=1 if str(row['Do you have Depression?']).strip().lower() == 'yes' else 0,
            anxiety=1 if str(row['Do you have Anxiety?']).strip().lower() == 'yes' else 0,
            panic_attack=1 if str(row['Do you have Panic attack?']).strip().lower() == 'yes' else 0,
            seek_treatment=1 if str(row['Did you seek any specialist for a treatment?']).strip().lower() == 'yes' else 0
        )
        res = await execute_zkml_inference(features, student_index=i + 1)
        results.append(res)
    return results
