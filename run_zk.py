import pandas as pd
import subprocess
import os
import shutil
from pydantic import BaseModel

class ZKP(BaseModel):
    student_index: int
    age: int
    status_message: str
    message: str

def get_student(count: int):
    print("🚀 เริ่มต้นโปรเจกต์ zkp_mental...")
    results = []
    
    # 1. อ่านข้อมูลจากไฟล์ CSV
    if not os.path.exists('student_mental_health.csv'):
        print("Not found file name: student_mental_health.csv")
        return results

    # ค้นหาตำแหน่งของคำสั่ง nargo
    nargo_bin = shutil.which("nargo")
    if not nargo_bin:
        expanded_path = os.path.expanduser("~/.nargo/bin/nargo")
        if os.path.exists(expanded_path):
            nargo_bin = expanded_path
        else:
            nargo_bin = "nargo"

    df = pd.read_csv('student_mental_health.csv')
    for i in range(min(count, len(df))):
        student_data = df.iloc[i]
        print(f'------------------------ ( คนที่ {i + 1} ) ---------------------------------')
        print("\n📊 [ข้อมูลดิบของนักศึกษาจาก CSV]")
        print(f"อายุ: {student_data['Age']}, ซึมเศร้า: {student_data['Do you have Depression?']}, วิตกกังวล: {student_data['Do you have Anxiety?']}, แพนิค: {student_data['Do you have Panic attack?']}")
        # 3. แปลงข้อมูลดิบ (Text) ให้เป็นตัวเลขฐานที่ ZK เข้าใจ
        age = int(student_data['Age'])
        depression = 1 if student_data['Do you have Depression?'] == 'Yes' else 0
        anxiety = 1 if student_data['Do you have Anxiety?'] == 'Yes' else 0
        panic_attack = 1 if student_data['Do you have Panic attack?'] == 'Yes' else 0

        # 4. เขียนข้อมูลลงใน Prover.toml ของ Noir อัตโนมัติ
        toml_content = f"""# ข้อมูลนี้จะถูกเก็บเป็นความลับ (Private)
        age = {age}
        depression = {depression}
        anxiety = {anxiety}
        panic_attack = {panic_attack}

        # เกณฑ์ที่มหาวิทยาลัยกำหนด (Public)
        min_age = 18
        """
        
        with open("circuit/Prover.toml", "w") as f:
            f.write(toml_content)
        print("📝 เขียนข้อมูลลงใน Prover.toml สำเร็จ")

        # 5. สั่งสั่งสร้าง Proof (สวมบทบาทเป็นนักศึกษา กดปุ่มส่งหลักฐาน)
        print("\n⏳ กำลังใช้คณิตศาสตร์ ZK คำนวณเพื่อสร้าง Proof...")
        
        result_prove = subprocess.run([nargo_bin, "execute"], cwd="circuit", capture_output=True, text=True)
        
        if result_prove.returncode != 0:
            msg = "ไม่ผ่านเกณฑ์อนุมัติสวัสดิการ (ข้อมูลไม่ตรงตามเงื่อนไขอายุหรือสุขภาพจิต)"
            print(f"❌ [ผลลัพธ์] ผลการตรวจสอบ: {msg}")
            results.append(ZKP(
                student_index=i + 1,
                age=age,
                status_message="Not Pass",
                message=  msg
            ))
            continue
            
        print("✅ คำนวณและสร้าง ZK Circuit Execution สำเร็จแล้ว!")

        # 6. สั่งตรวจสอบ (สวมบทบาทเป็นมหาวิทยาลัย)
        print("\n🔍 มหาวิทยาลัยกำลังทำการตรวจสอบความถูกต้องผ่านสคริปต์ทดสอบ...")
        result_verify = subprocess.run([nargo_bin, "test"], cwd="circuit", capture_output=True, text=True)
        
        if result_verify.returncode == 0:
            msg = "ผ่านเกณฑ์อนุมัติสวัสดิการ! โดยไม่เปิดเผยข้อมูลส่วนตัว"
            print(f"🎉 [ผลลัพธ์] ผลการตรวจสอบ: {msg}")
            results.append(ZKP(
                student_index=i + 1,
                age=age,
                status_message="Pass",
                message=msg
            ))
        else:
            msg = "ข้อมูลไม่ตรงตามเงื่อนไข"
            print(f"❌ [ผลลัพธ์] ผลการตรวจสอบ: {msg}")
            results.append(ZKP(
                student_index=i + 1,
                age=age,
                status_message="Not Match Data",
                message=msg
            ))

    return results

if __name__ == "__main__":
    get_student(1)