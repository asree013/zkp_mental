"""
ML Model Management & Integer Quantization Module
=================================================
จัดการการโหลดข้อมูล การฝึกสอนโมเดล Logistic Regression และการทำ Quantization 
แปลงค่าน้ำหนัก (Weights & Bias) เป็นตัวเลขจำนวนเต็มสำหรับ Noir ZK Circuit
"""

import json
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression


def parse_cgpa(cgpa_val: str) -> int:
    """
    แปลงช่วง CGPA แบบข้อความ เป็นค่าสเกลตัวเลขจำนวนเต็ม (Scaled Integer x 100)
    ตัวอย่าง: '3.50 - 4.00' -> 375, '3.00 - 3.49' -> 325
    """
    if not isinstance(cgpa_val, str):
        return 325
    s = cgpa_val.strip()
    if '3.50' in s:
        return 375
    elif '3.00' in s:
        return 325
    elif '2.50' in s:
        return 275
    elif '2.00' in s:
        return 225
    elif '0' in s:
        return 100
    return 325


def preprocess_dataset(csv_path: str = 'student_mental_health.csv') -> pd.DataFrame:
    """
    โหลดและทำความสะอาดข้อมูลสุขภาพจิตนักเรียนจากไฟล์ CSV
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"ไม่พบไฟล์ข้อมูลแบบสำรวจ: {csv_path}")

    df = pd.read_csv(csv_path)

    # 1. แปลงอายุเป็นตัวเลขจำนวนเต็ม (ใช้ 20 เป็นค่าเริ่มต้นหากมี null)
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(20).astype(int)

    # 2. แปลง CGPA เป็น Quantized Scale
    df['CGPA_Scaled'] = df['What is your CGPA?'].apply(parse_cgpa)

    # 3. แปลงภาวะสุขภาพจิตเป็น Binary (1 = Yes, 0 = No)
    df['Depression'] = df['Do you have Depression?'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    df['Anxiety'] = df['Do you have Anxiety?'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    df['Panic_Attack'] = df['Do you have Panic attack?'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    df['Seek_Treatment'] = df['Did you seek any specialist for a treatment?'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)

    # 4. สร้าง Target Label: 1 = มีภาวะเสี่ยงสุขภาพจิต / ต้องการคำปรึกษา, 0 = สภาวะปกติ
    df['Target_Risk'] = (
        (df['Depression'] == 1) | 
        (df['Anxiety'] == 1) | 
        (df['Panic_Attack'] == 1) | 
        (df['Seek_Treatment'] == 1)
    ).astype(int)

    return df


def train_and_quantize(csv_path: str = 'student_mental_health.csv', scaling_factor: int = 1000) -> dict:
    """
    ฝึกสอนโมเดล Logistic Regression และแปลงค่าน้ำหนักเป็น Quantized Integers
    บันทึกผลลัพธ์เป็นไฟล์ model_weights.json
    """
    df = preprocess_dataset(csv_path)

    feature_cols = ['Age', 'CGPA_Scaled', 'Depression', 'Anxiety', 'Panic_Attack', 'Seek_Treatment']
    X = df[feature_cols]
    y = df['Target_Risk']

    # เทรนโมเดล Logistic Regression
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    # สกัดค่าน้ำหนักดิบ (Floating-point)
    raw_weights = model.coef_[0]
    raw_bias = float(model.intercept_[0])

    # แปลงค่าน้ำหนักเป็น Integer Quantized Value (คูณ scaling_factor)
    quantized_weights = [int(round(w * scaling_factor)) for w in raw_weights]
    quantized_bias = int(round(raw_bias * scaling_factor))
    quantized_threshold = 0  # Linear Decision Boundary ที่ 0

    model_metadata = {
        "model_type": "Quantized Logistic Regression Classifier",
        "scaling_factor": scaling_factor,
        "feature_names": feature_cols,
        "raw_weights": raw_weights.tolist(),
        "raw_bias": raw_bias,
        "quantized_weights": quantized_weights,
        "quantized_bias": quantized_bias,
        "quantized_threshold": quantized_threshold,
        "accuracy": float(model.score(X, y)),
        "dataset_samples": len(df)
    }

    # บันทึกไฟล์ JSON
    output_path = 'model_weights.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(model_metadata, f, indent=2, ensure_ascii=False)

    print("=========================================================")
    print("✅ ฝึกสอนและแปลง Quantization โมเดล ZK-ML สำเร็จ!")
    print(f"📊 ขนาดข้อมูล: {len(df)} ตัวอย่าง | ความแม่นยำ (Accuracy): {model_metadata['accuracy'] * 100:.2f}%")
    print(f"⚖️ Quantized Weights: {quantized_weights}")
    print(f"🎯 Quantized Bias: {quantized_bias}")
    print(f"💾 บันทึกโมเดลลงไฟล์: {output_path}")
    print("=========================================================")

    return model_metadata


def load_model_weights(output_path: str = 'model_weights.json') -> dict:
    """
    โหลดข้อมูลพารามิเตอร์โมเดล ML หากไม่มีไฟล์จะทำการเทรนใหม่อัตโนมัติ
    """
    if not os.path.exists(output_path):
        return train_and_quantize()
    with open(output_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    train_and_quantize()
