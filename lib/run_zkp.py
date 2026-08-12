"""
CLI Tool: Run ZK-ML Circuit Execution Sample
==============================================
สคริปต์ทดสอบประมวลผล ZK-ML Inference จากข้อมูลตัวอย่าง (lib/run_zkp.py)

วิธีรัน:
python lib/run_zkp.py
"""

import sys
import os
import asyncio

# เพิ่ม Root Directory เข้า sys.path เพื่อให้อ่านโมดูล app ได้ถูกต้องเมื่อรันตรง
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.services.zk_service import get_student_sample_zk

def main(count: int = 1):
    print(f"⚡ สั่งประมวลผล ZK-ML Inference สำหรับข้อมูลตัวอย่างนักเรียน ({count} ราย)...")
    results = asyncio.run(get_student_sample_zk(count))
    for res in results:
        print("\n---------------------------------------------------------")
        print(f"🎓 นักเรียนลำดับที่: {res.student_index}")
        print(f"🛡️ สถานะ ZK Proof: {res.verification_status}")
        print(f"📊 ผลประเมินความเสี่ยง (Risk Class): {res.risk_class} ({res.risk_label})")
        print(f"⏱️ เวลาที่ใช้สร้าง Proof: {res.proving_time_ms} ms")
        print(f"💬 รายละเอียด: {res.message}")
        print("---------------------------------------------------------")

if __name__ == '__main__':
    count_arg = 1
    if len(sys.argv) > 1:
        try:
            count_arg = int(sys.argv[1])
        except ValueError:
            count_arg = 1
    main(count_arg)
