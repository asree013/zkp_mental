"""
CLI Tool: Train & Quantize ML Model for ZK Circuit
===================================================
สคริปต์รันการเทรนโมเดล ML และทำ Integer Quantization (lib/train_ml_model.py)

วิธีรัน:
python lib/train_ml_model.py
"""

import sys
import os

# เพิ่ม Root Directory เข้า sys.path เพื่อให้อ่านโมดูล app ได้ถูกต้องเมื่อรันตรง
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.models.ml_model import train_and_quantize

def main():
    print("🚀 เริ่มต้นกระบวนการฝึกสอนโมเดล ML และทำ Quantization...")
    train_and_quantize()

if __name__ == '__main__':
    main()
