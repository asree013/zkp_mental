fn main(
    // ใน Noir เวอร์ชันใหม่ ตัวแปรที่ไม่มีอะไรนำหน้าจะถือว่าเป็น Private (ความลับ) ทันที
    age: u8,
    depression: u8,    // 1 = Yes, 0 = No
    anxiety: u8,       // 1 = Yes, 0 = No
    panic_attack: u8,  // 1 = Yes, 0 = No

    // ตัวแปรไหนที่ต้องการให้เป็น Public (เปิดเผย) ให้ใช้คีย์เวิร์ด pub นำหน้าประเภทตัวแปร
    min_age: pub u8
) {
    // 1. ตรวจสอบว่าอายุไม่ต่ำกว่าเกณฑ์
    assert(age >= min_age);

    // 2. ตรวจสอบว่ามีภาวะเสี่ยงอย่างน้อย 1 อย่าง (ผลรวมต้องมากกว่า 0)
    let total_risk = depression + anxiety + panic_attack;
    assert(total_risk > 0);
}