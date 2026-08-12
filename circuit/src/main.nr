fn main(
    // -------------------------------------------------------------
    // PRIVATE INPUTS ( Sensitive Student Mental Health Features )
    // ข้อมูลสุขภาพจิตส่วนบุคคล (เก็บเป็นความลับ ไม่ถูกเปิดเผยภายนอก)
    // -------------------------------------------------------------
    age: u8,
    cgpa_scaled: u16,
    depression: u8,
    anxiety: u8,
    panic_attack: u8,
    seek_treatment: u8,

    // -------------------------------------------------------------
    // PUBLIC INPUTS ( Quantized ML Model Weights & Criteria )
    // น้ำหนักโมเดล ML และเกณฑ์การประเมินที่เป็นมาตรฐานสาธารณะ
    // -------------------------------------------------------------
    weights: pub [i32; 6],
    bias: pub i32,
    threshold: pub i32,
    expected_risk_class: pub u8
) {
    // 1. ตรวจสอบ Range ความถูกต้องของข้อมูลป้อนเข้าเบื้องต้น
    assert(age >= 15);
    assert(age <= 100);

    // 2. คำนวณ ZK-ML Score ด้วย Integer Linear Combination
    let score: i32 = (age as i32 * weights[0])
                   + (cgpa_scaled as i32 * weights[1])
                   + (depression as i32 * weights[2])
                   + (anxiety as i32 * weights[3])
                   + (panic_attack as i32 * weights[4])
                   + (seek_treatment as i32 * weights[5])
                   + bias;

    // 3. จำแนกความเสี่ยงสุขภาพจิตตามเกณฑ์ของโมเดล (0 = Low Risk, 1 = High Risk)
    let computed_risk: u8 = if score >= threshold { 1 } else { 0 };

    // 4. พิสูจน์ด้วย ZK ว่าผลการจำแนกตรงกับ expected_risk_class ที่ระบุ
    assert(computed_risk == expected_risk_class);
}