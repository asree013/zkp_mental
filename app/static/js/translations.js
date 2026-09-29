/**
 * Multi-Language (i18n) Engine & Dictionaries (TH / EN)
 * Privacy-Preserving ZK-ML Student Mental Health Research Platform
 * Path: app/static/js/translations.js
 */

const I18N_DICTIONARIES = {
    th: {
        // Brand & Header
        "brand_title": "ZK-ML Research Platform",
        "brand_sub": "ระบบวิจัยการอนุมานรักษาความเป็นส่วนตัวบนข้อมูลสุขภาพจิตนักเรียน",
        
        // Navigation Links
        "nav_home": "หน้าแรก",
        "nav_students": "ข้อมูลนักเรียน & CSV",
        "nav_papers": "เอกสารงานวิจัย",
        "nav_quant": "Quantization Benchmark",
        "nav_crypto": "Cryptographic Benchmark",
        "nav_compare": "เปรียบเทียบ ZKP vs ZK-ML",
        "nav_weights": "พารามิเตอร์โมเดล",
        "nav_docs": "Swagger Docs",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "toggle_theme_title": "สลับโหมด มืด / สว่าง (Toggle Dark/Light Mode)",
        "toggle_lang_title": "สลับภาษา (Switch Language: TH / EN)",

        // Academic Hero Section (Home)
        "academic_degree_badge": "M.Sc. Data Science",
        "academic_thesis_tag": "วิทยานิพนธ์ระดับปริญญาโท (Master's Thesis แผน ก แบบ ก 2)",
        "student_id_label": "รหัสนักศึกษา:",
        "degree_label": "หลักสูตร:",
        "faculty_label": "สังกัด:",
        "thesis_title_label": "ชื่อหัวข้อวิทยานิพนธ์ (Official Research Title)",

        // IEEE Paper & Proposal Showcase
        "ieee_section_title": "เอกสารงานวิจัยมาตรฐาน IEEE (IEEE Research Paper)",
        "ieee_section_sub": "งานวิจัยการอนุมานโมเดลแบบรักษาความเป็นส่วนตัวด้วย ZK-ML ตามรูปแบบมาตรฐาน IEEE",
        "empty_ieee_title": "ยังไม่มีการอัปโหลดเอกสาร IEEE Paper เข้าสู่ระบบ",
        "empty_ieee_desc": "คุณสามารถอัปโหลดไฟล์ PDF งานวิจัยประเภท IEEE Paper ได้ที่หน้าจัดการเอกสารงานวิจัย",
        "btn_upload_ieee": "อัปโหลด IEEE Paper ตอนนี้",
        "proposal_section_title": "เอกสารโครงร่างวิทยานิพนธ์ (Thesis Proposal Document)",
        "proposal_section_sub": "ฉบับล่าสุดสำหรับการสอบโครงร่างและพัฒนาโมเดล ZK-ML",
        "latest_badge": "ฉบับล่าสุด (Latest)",
        "open_new_tab": "เปิดแท็บใหม่",
        "download_pdf": "ดาวน์โหลด PDF",
        "manage_all_docs": "จัดการเอกสารทั้งหมด",
        "filename_label": "ชื่อไฟล์:",
        "uploaded_at_label": "อัปโหลดเมื่อ:",
        "empty_proposal_title": "ยังไม่มีเอกสารโครงร่างวิทยานิพนธ์ในระบบ",
        "empty_proposal_desc": "คุณสามารถอัปโหลดไฟล์ PDF โครงร่างวิทยานิพนธ์ได้ในหน้าจัดการเอกสารงานวิจัย",

        // Portals Section
        "portals_title": "โมดูลระบบวิจัยและเครื่องมือทดสอบ",
        "portals_sub": "เข้าถึงโมดูลการทดลอง, REST API Documentation, และสถิติเชิงปริมาณของงานวิจัย",
        "portal_students_title": "Student Data & CSV Ingestion",
        "portal_students_desc": "ระบบจัดการฐานข้อมูลนักเรียน: เพิ่มข้อมูลรายคน, อัปโหลด Batch CSV, ลบข้อมูล และทดสอบ ZK Proof รายบุคคล",
        "portal_students_action": "จัดการข้อมูลนักเรียน",
        "portal_quant_title": "Quantization Impact Benchmark",
        "portal_quant_desc": "วิเคราะห์ผลกระทบของ Integer Quantization ตารางเปรียบเทียบ Scaling Factors และกราฟสำหรับเล่มวิจัยบทที่ 4",
        "portal_quant_action": "เข้าสู่หน้า Dashboard",
        "portal_crypto_title": "Cryptographic & ZK Benchmark",
        "portal_crypto_desc": "วิเคราะห์ ACIR Constraints (312 Opcodes), Latency Distribution, Throughput และ Feature Scaling O(N)",
        "portal_crypto_action": "ดูสถิติ Cryptography",
        "portal_compare_title": "Compare Plain ZKP vs ZK-ML",
        "portal_compare_desc": "ทดสอบเปรียบเทียบ Side-by-Side ระหว่างระบบกฎเกณฑ์ธรรมดากับ ZK-ML เพื่อพิสูจน์คุณค่างานวิจัยบทที่ 4",
        "portal_compare_action": "เข้าสู่หน้าเปรียบเทียบ",
        "portal_docs_title": "Interactive REST API Docs",
        "portal_docs_desc": "เอกสาร OpenAPI / Swagger UI สำหรับทดสอบส่ง Request สร้าง ZK Proof และเรียกดูข้อมูลโมเดลแบบ Real-time",
        "portal_docs_action": "เปิดเอกสาร Swagger",
        "portal_weights_title": "Public Model Weights & Bias",
        "portal_weights_desc": "ดึงค่าสัมประสิทธิ์ค่าน้ำหนัก Quantized Weights, Threshold และ Metadata ของโมเดลในรูปแบบ JSON API",
        "portal_weights_action": "ดู JSON Metadata",

        // Interactive Live ZK-ML Tester
        "tester_title": "ทดสอบรันการประมวลผล ZK-ML สด (Live Interactive ZK Prover)",
        "tester_desc": "จำลองการส่งข้อมูลสุขภาพจิตเข้าสู่วงจร Noir Circuit เพื่อสร้างและยืนยัน ZK Proof โดยข้อมูลส่วนบุคคลจะไม่รั่วไหล",
        "tester_privacy_shield": "ระบบรักษาความเป็นส่วนตัวทำงาน (Privacy Shield Active)",
        "label_age": "อายุ (Age)",
        "label_cgpa": "ช่วงเกรดเฉลี่ย (CGPA Range)",
        "label_depression": "ภาวะซึมเศร้า (Depression)",
        "label_anxiety": "ภาวะวิตกกังวล (Anxiety)",
        "label_panic": "อาการตื่นตระหนก (Panic Attack)",
        "label_treatment": "เคยรับการปรึกษา/รักษา (Seek Treatment)",
        "cgpa_opt_excellent": "3.50 - 4.00 (ยอดเยี่ยม)",
        "cgpa_opt_good": "3.00 - 3.49 (ดี)",
        "cgpa_opt_fair": "2.50 - 2.99 (ปานกลาง)",
        "cgpa_opt_pass": "2.00 - 2.49 (พอใช้)",
        "cgpa_opt_critical": "0 - 1.99 (วิกฤต)",
        "option_yes": "มีอาการ (Yes)",
        "option_no": "ไม่มีอาการ (No)",
        "btn_run_zk": "เริ่มทดสอบสร้างและพิสูจน์ Zero-Knowledge Proof",
        "running_proof": "กำลังสร้างพยานหลักฐานและพิสูจน์ ZK Proof (Nargo Prover)...",
        "result_box_title": "ผลการประมวลผล Zero-Knowledge Proof (ZK Verification Result)",
        "result_status_label": "สถานะการตรวจสอบ (ZK Verification)",
        "result_pred_label": "การทำนายความเสี่ยง (Predicted Risk)",
        "result_latency_label": "เวลาสร้าง Proof (Proving Latency)",
        "result_constraints_label": "ขนาดวงจร (Circuit Constraints)",
        "result_valid": "ผ่านการตรวจสอบ (Valid Proof)",
        "result_invalid": "ไม่ผ่านการตรวจสอบ (Invalid Proof)",
        "risk_high": "กลุ่มเสี่ยง (High Risk)",
        "risk_low": "กลุ่มปกติ (Low Risk)",

        // Student Data Page
        "students_page_title": "ระบบจัดการข้อมูลสุขภาพจิตนักเรียน (Student Mental Health Database)",
        "students_page_desc": "จัดการข้อมูลนักเรียนในฐานข้อมูล MySQL, อัปโหลดชุดข้อมูล Batch CSV, และทดสอบการอนุมาน ZK-ML รายคน",
        "btn_add_student": "เพิ่มข้อมูลนักเรียน",
        "btn_add_student_title": "เพิ่มข้อมูลนักเรียนรายคน (Manual Entry)",
        "btn_upload_csv": "อัปโหลดไฟล์ CSV",
        "btn_import_csv_title": "อัปโหลดชุดข้อมูล CSV (Batch Ingestion)",
        "btn_clear_all": "ล้างข้อมูลทั้งหมด",
        "btn_clear_all_title": "ล้างข้อมูลทั้งหมดในฐานข้อมูล",
        "search_student_placeholder": "ค้นหาตาม ID, อายุ, ระดับการศึกษา, สาขาวิชา, CGPA...",
        "filter_all": "ทั้งหมด",
        "filter_risk_high": "กลุ่มเสี่ยงสูง",
        "filter_risk_low": "กลุ่มปกติ",
        "table_col_id": "รหัส (ID)",
        "table_col_age": "อายุ (Age)",
        "table_col_gender": "เพศ (Gender)",
        "table_col_course": "คณะ/สาขาวิชา",
        "table_col_year": "ชั้นปี",
        "table_col_cgpa": "เกรดเฉลี่ย (CGPA)",
        "table_col_depression": "ซึมเศร้า",
        "table_col_anxiety": "วิตกกังวล",
        "table_col_panic": "ตื่นตระหนก",
        "table_col_treatment": "การรักษา",
        "table_col_edu_level": "ระดับการศึกษา (Education Level)",
        "table_col_action": "การกระทำ (Actions)",
        "btn_test_row_zk": "ทดสอบ ZK",
        "btn_edit": "แก้ไข",
        "btn_delete": "ลบ",
        "stats_total_students": "นักเรียนทั้งหมด",
        "stats_high_risk": "กลุ่มเสี่ยงสูง (High Risk)",
        "stats_low_risk": "กลุ่มปกติ (Low Risk)",
        "stats_db_source": "แหล่งข้อมูล: MySQL Database",
        "stat_total_label": "ข้อมูลนักเรียนทั้งหมดในตาราง",
        "stat_high_risk_label": "High Risk Cases (มีภาวะเสี่ยง)",
        "stat_high_risk_desc": "นักเรียนที่มีภาวะ Depression / Anxiety หรือ Panic Attack",
        "stat_low_risk_label": "Low Risk Cases (ปกติ)",
        "stat_low_risk_desc": "นักเรียนที่ไม่มีภาวะเสี่ยงสุขภาพจิต",
        "stat_seek_treatment_label": "Specialist Treatment (เคยพบแพทย์)",
        "stat_seek_treatment_desc": "นักเรียนที่เคยปรึกษาผู้เชี่ยวชาญด้านสุขภาพจิต",
        "student_table_header": "ตารางข้อมูลสุขภาพจิตนักเรียน (Mental Health Records)",
        "student_table_desc": "ระบบค้นหาแบบละเอียด, คัดกรองระดับการศึกษา/ภาวะเสี่ยง พร้อมระบบแบ่งหน้า (Pagination)",
        "th_student_id": "ID",
        "th_student_age": "อายุ / เพศ (Age / Gender)",
        "th_student_gender": "เพศ (Gender)",
        "th_student_course": "คณะ & ชั้นปี (Course & Year)",
        "th_student_year": "ชั้นปี (Year)",
        "th_student_cgpa": "CGPA",
        "th_student_depression": "ซึมเศร้า (Depression)",
        "th_student_anxiety": "วิตกกังวล (Anxiety)",
        "th_student_panic": "แพนิค (Panic)",
        "th_student_treatment": "การรักษา (Treatment)",
        "th_student_edu": "ระดับการศึกษา (Education Level)",
        "th_student_action": "การกระทำ (Actions)",
        "students_unit_persons": "คน",

        // Paper Page
        "paper_page_title": "ระบบจัดการเอกสารงานวิจัยและวิทยานิพนธ์ (Research Papers)",
        "paper_page_desc": "อัปโหลด จัดหมวดหมู่บทที่ 1-5 โครงร่างวิทยานิพนธ์ และพรีวิวเอกสาร PDF พร้อมระบบรักษาความปลอดภัยในการลบข้อมูล",
        "btn_upload_paper": "อัปโหลดเอกสารใหม่",
        "btn_upload_new_paper": "อัปโหลดเอกสารใหม่",
        "upload_box_title": "อัปโหลดไฟล์ PDF งานวิจัย",
        "upload_type_label": "หมวดหมู่งานวิจัย / ประเภทเอกสาร",
        "paper_table_title": "รายการเอกสารงานวิจัยในระบบ",
        "paper_table_desc": "คลิกดูตัวอย่างไฟล์ (Preview), แก้ไขข้อมูล หรือคัดลอก Link เข้าถึงเอกสาร",
        "paper_search_placeholder": "ค้นหาชื่อเอกสาร หรือบท...",
        "filter_tab_all": "ทั้งหมด",
        "filter_tab_chap1": "บทที่ 1",
        "filter_tab_chap2": "บทที่ 2",
        "filter_tab_chap3": "บทที่ 3",
        "filter_tab_chap4": "บทที่ 4",
        "filter_tab_chap5": "บทที่ 5",
        "filter_tab_proposal": "Proposal",
        "filter_tab_full": "เล่มเต็ม",
        "filter_tab_recommend": "ข้อเสนอแนะ",
        "filter_tab_ieee": "IEEE Paper",
        "filter_tab_project": "Project Paper",
        "th_col_category": "หมวดหมู่ / บท",
        "th_col_title": "ชื่อเอกสาร",
        "th_col_link": "URL Link เข้าถึงไฟล์",
        "th_col_date": "วันที่อัปโหลด",
        "th_col_actions": "การจัดการ",
        "paper_col_title": "ชื่อเอกสาร",
        "paper_col_type": "ประเภท",
        "paper_col_uploaded": "วันที่อัปโหลด",
        "paper_col_size": "ขนาดไฟล์",
        "paper_col_actions": "การกระทำ",
        "paper_stat_total": "เอกสารทั้งหมด",
        "paper_stat_chapters": "บทที่ 1 - 5",
        "paper_stat_proposals": "โครงร่าง / Proposal",
        "paper_stat_all": "เล่มสมบูรณ์ / IEEE / โครงงาน",

        // Metrics & Benchmarks
        "metric_acc_desc": "ความแม่นยำหลัง Quantize ใน ZK Circuit โดยไม่มีการสูญเสียความแม่นยำ (Delta = 0.0%)",
        "metric_priv_desc": "ข้อมูลสุขภาพจิตนักเรียนทุกตัวแปรถูกเก็บเป็นความลับใน Noir Circuit ไม่ถูกเปิดเผยภายนอก",
        "metric_scale_desc": "สเกลที่ให้ความแม่นยำสูงสุดและลด Score Drift MAE เหลือ 0.08 ปลอดภัยจาก Integer Overflow",
        "metric_engine_desc": "Nargo CLI พร้อมประมวลผล Asynchronous ZK Proof ร่วมกับ Hybrid Database Provider",
        "quant_title": "Integer Quantization Impact Benchmark",
        "quant_desc": "วิเคราะห์ผลกระทบของ Scaling Factor ต่อความแม่นยำ (Accuracy, F1-Score, MAE) ในวงจร ZK-ML",
        "crypto_title": "Cryptographic & Circuit Performance Benchmark",
        "crypto_desc": "วิเคราะห์ประสิทธิภาพการคำนวณด้านวิทยาการรหัสลับ ACIR Constraints, Proving Time, และ Throughput",
        "compare_title": "Side-by-Side Comparison: Plain ZKP vs ZK-ML",
        "compare_desc": "การเปรียบเทียบเชิงวิชาการระหว่าง Rule-Based Heuristic กับ Machine Learning Inference ใน Zero-Knowledge Proofs"
    },
    en: {
        // Brand & Header
        "brand_title": "ZK-ML Research Platform",
        "brand_sub": "Privacy-Preserving Inference for Student Mental Health",

        // Navigation Links
        "nav_home": "Home",
        "nav_students": "Student Data & CSV",
        "nav_papers": "Research Papers",
        "nav_quant": "Quantization Benchmark",
        "nav_crypto": "Cryptographic Benchmark",
        "nav_compare": "Compare ZKP vs ZK-ML",
        "nav_weights": "Model Weights",
        "nav_docs": "Swagger Docs",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "toggle_theme_title": "Toggle Dark / Light Mode",
        "toggle_lang_title": "Switch Language: English / Thai",

        // Academic Hero Section (Home)
        "academic_degree_badge": "M.Sc. Data Science",
        "academic_thesis_tag": "Master's Thesis (Plan A, Type A2)",
        "student_id_label": "Student ID:",
        "degree_label": "Degree Program:",
        "faculty_label": "Affiliation:",
        "thesis_title_label": "Official Research Title",

        // IEEE Paper & Proposal Showcase
        "ieee_section_title": "IEEE Standard Research Paper",
        "ieee_section_sub": "Privacy-Preserving Machine Learning Inference using ZK-Proofs (IEEE Standard Format)",
        "empty_ieee_title": "No IEEE Paper uploaded yet",
        "empty_ieee_desc": "You can upload an IEEE Paper PDF in the research papers management section.",
        "btn_upload_ieee": "Upload IEEE Paper Now",
        "proposal_section_title": "Thesis Proposal Document",
        "proposal_section_sub": "Latest version for thesis proposal defense & ZK-ML model evaluation",
        "latest_badge": "Latest Edition",
        "open_new_tab": "Open New Tab",
        "download_pdf": "Download PDF",
        "manage_all_docs": "Manage All Documents",
        "filename_label": "Filename:",
        "uploaded_at_label": "Uploaded at:",
        "empty_proposal_title": "No thesis proposal document found",
        "empty_proposal_desc": "You can upload a thesis proposal PDF in the research paper management section.",

        // Portals Section
        "portals_title": "Research Modules & Testing Tools",
        "portals_sub": "Access experimental benchmark modules, REST API Documentation, and quantitative metrics",
        "portal_students_title": "Student Data & CSV Ingestion",
        "portal_students_desc": "Student database management: Single records, batch CSV ingestion, deletion, and individual ZK proof testing",
        "portal_students_action": "Manage Student Data",
        "portal_quant_title": "Quantization Impact Benchmark",
        "portal_quant_desc": "Analyze integer quantization impact, scaling factor comparison table, and graphs for Thesis Chapter 4",
        "portal_quant_action": "Enter Dashboard",
        "portal_crypto_title": "Cryptographic & ZK Benchmark",
        "portal_crypto_desc": "Analyze ACIR constraints (312 opcodes), latency distribution, throughput, and O(N) feature scaling",
        "portal_crypto_action": "View Cryptography Stats",
        "portal_compare_title": "Compare Plain ZKP vs ZK-ML",
        "portal_compare_desc": "Side-by-side empirical comparison between rule-based heuristics and ZK-ML for Chapter 4 justification",
        "portal_compare_action": "Enter Comparison",
        "portal_docs_title": "Interactive REST API Docs",
        "portal_docs_desc": "OpenAPI / Swagger UI docs for testing requests, generating ZK proofs, and querying models in real-time",
        "portal_docs_action": "Open Swagger Docs",
        "portal_weights_title": "Public Model Weights & Bias",
        "portal_weights_desc": "Fetch quantized coefficients, weights, bias, threshold, and model metadata via JSON API",
        "portal_weights_action": "View JSON Metadata",

        // Interactive Live ZK-ML Tester
        "tester_title": "Live Interactive ZK-ML Inference Tester (Noir Prover)",
        "tester_desc": "Simulate passing mental health features into Noir Circuit to generate and verify ZK Proof without private data leakage",
        "tester_privacy_shield": "Privacy Shield Active",
        "label_age": "Age",
        "label_cgpa": "CGPA Range",
        "label_depression": "Depression",
        "label_anxiety": "Anxiety",
        "label_panic": "Panic Attack",
        "label_treatment": "Sought Treatment",
        "cgpa_opt_excellent": "3.50 - 4.00 (Excellent)",
        "cgpa_opt_good": "3.00 - 3.49 (Good)",
        "cgpa_opt_fair": "2.50 - 2.99 (Fair)",
        "cgpa_opt_pass": "2.00 - 2.49 (Passing)",
        "cgpa_opt_critical": "0 - 1.99 (Critical)",
        "option_yes": "Yes (Positive)",
        "option_no": "No (Negative)",
        "btn_run_zk": "Generate & Verify Zero-Knowledge Proof",
        "running_proof": "Generating witness and verifying ZK Proof via Nargo Prover...",
        "result_box_title": "Zero-Knowledge Proof Verification Result",
        "result_status_label": "ZK Verification Status",
        "result_pred_label": "Predicted Risk",
        "result_latency_label": "Proving Latency",
        "result_constraints_label": "Circuit Constraints",
        "result_valid": "Verification Passed (Valid Proof)",
        "result_invalid": "Verification Failed (Invalid Proof)",
        "risk_high": "High Risk Group",
        "risk_low": "Low Risk / Normal Group",

        // Student Data Page
        "students_page_title": "Student Mental Health Database Management",
        "students_page_desc": "Manage student records in MySQL, ingest batch CSV datasets, and execute individual ZK-ML inference",
        "btn_add_student": "Add Student Record",
        "btn_add_student_title": "Add Student Record (Manual Entry)",
        "btn_upload_csv": "Upload CSV File",
        "btn_import_csv_title": "Upload CSV Dataset (Batch Ingestion)",
        "btn_clear_all": "Clear All Records",
        "btn_clear_all_title": "Clear All Records in Database",
        "search_student_placeholder": "Search by ID, Age, Education Level, Course, CGPA...",
        "filter_all": "All",
        "filter_risk_high": "High Risk",
        "filter_risk_low": "Low Risk",
        "table_col_id": "ID",
        "table_col_age": "Age",
        "table_col_gender": "Gender",
        "table_col_course": "Course / Major",
        "table_col_year": "Year",
        "table_col_cgpa": "CGPA",
        "table_col_depression": "Depression",
        "table_col_anxiety": "Anxiety",
        "table_col_panic": "Panic Attack",
        "table_col_treatment": "Treatment",
        "table_col_edu_level": "Education Level",
        "table_col_action": "Actions",
        "btn_test_row_zk": "Test ZK",
        "btn_edit": "Edit",
        "btn_delete": "Delete",
        "stats_total_students": "Total Students",
        "stats_high_risk": "High Risk Group",
        "stats_low_risk": "Low Risk Group",
        "stats_db_source": "Source: MySQL Database",
        "stat_total_label": "Total Student Records in Table",
        "stat_high_risk_label": "High Risk Cases",
        "stat_high_risk_desc": "Students with Depression, Anxiety, or Panic Attacks",
        "stat_low_risk_label": "Low Risk Cases (Normal)",
        "stat_low_risk_desc": "Students with no mental health risk history",
        "stat_seek_treatment_label": "Specialist Treatment",
        "stat_seek_treatment_desc": "Students who consulted a mental health specialist",
        "student_table_header": "Student Mental Health Records Table",
        "student_table_desc": "Detailed search, education level & risk filtering with pagination",
        "th_student_id": "ID",
        "th_student_age": "Age / Gender",
        "th_student_gender": "Gender",
        "th_student_course": "Course & Year",
        "th_student_year": "Year",
        "th_student_cgpa": "CGPA",
        "th_student_depression": "Depression",
        "th_student_anxiety": "Anxiety",
        "th_student_panic": "Panic",
        "th_student_treatment": "Treatment",
        "th_student_edu": "Education Level",
        "th_student_action": "Actions",
        "students_unit_persons": "students",

        // Paper Page
        "paper_page_title": "Research Papers & Proposal Repository",
        "paper_page_desc": "Store, organize, and manage thesis proposals, research papers, and defense slide decks (PDF Files)",
        "btn_upload_paper": "Upload New Paper",
        "btn_upload_new_paper": "Upload New Paper",
        "upload_box_title": "Upload Research Paper PDF",
        "upload_type_label": "Paper Category / Document Type",
        "paper_table_title": "Research Papers in Repository",
        "paper_table_desc": "Click Preview to view document, edit metadata, or copy file access link",
        "paper_search_placeholder": "Search paper title or chapter...",
        "filter_tab_all": "All",
        "filter_tab_chap1": "Chapter 1",
        "filter_tab_chap2": "Chapter 2",
        "filter_tab_chap3": "Chapter 3",
        "filter_tab_chap4": "Chapter 4",
        "filter_tab_chap5": "Chapter 5",
        "filter_tab_proposal": "Proposal",
        "filter_tab_full": "Full Thesis",
        "filter_tab_recommend": "Recommendations",
        "filter_tab_ieee": "IEEE Paper",
        "filter_tab_project": "Project Paper",
        "th_col_category": "Category / Chapter",
        "th_col_title": "Document Title",
        "th_col_link": "Access URL Link",
        "th_col_date": "Upload Date",
        "th_col_actions": "Actions",
        "paper_col_title": "Document Title",
        "paper_col_type": "Type",
        "paper_col_uploaded": "Upload Date",
        "paper_col_size": "File Size",
        "paper_col_actions": "Actions",
        "paper_stat_total": "Total Documents",
        "paper_stat_chapters": "Chapters 1 - 5",
        "paper_stat_proposals": "Proposals",
        "paper_stat_all": "Full Theses / IEEE",

        // Metrics & Benchmarks
        "metric_acc_desc": "Post-quantization accuracy in ZK circuit with zero precision loss (Delta = 0.0%)",
        "metric_priv_desc": "All sensitive mental health inputs are private variables in Noir circuit, protected from leakage",
        "metric_scale_desc": "Optimal scale maximizing accuracy and reducing Score Drift MAE to 0.08 without overflow",
        "metric_engine_desc": "Nargo CLI asynchronous ZK prover engine with hybrid database provider fallback",
        "quant_title": "Integer Quantization Impact Benchmark",
        "quant_desc": "Analyze scaling factor impact on accuracy, F1-score, and MAE drift for Noir ZK-ML circuit",
        "crypto_title": "Cryptographic & Circuit Performance Benchmark",
        "crypto_desc": "Analyze cryptographic overhead, ACIR constraints, proving time, and system throughput",
        "compare_title": "Side-by-Side Comparison: Plain ZKP vs ZK-ML",
        "compare_desc": "Academic comparison between rule-based heuristics and machine learning inference within Zero-Knowledge Proofs"
    }
};

/**
 * Get translation for given key
 */
function t(key, defaultText = "") {
    const lang = getCurrentLanguage();
    if (I18N_DICTIONARIES[lang] && I18N_DICTIONARIES[lang][key]) {
        return I18N_DICTIONARIES[lang][key];
    }
    // If language is 'en', DO NOT fall back to 'th'!! Return defaultText or key
    if (lang === 'en') {
        return defaultText || (I18N_DICTIONARIES['en'] && I18N_DICTIONARIES['en'][key]) || key;
    }
    if (I18N_DICTIONARIES['th'] && I18N_DICTIONARIES['th'][key]) {
        return I18N_DICTIONARIES['th'][key];
    }
    return defaultText || key;
}

/**
 * Get current selected language ('th' or 'en')
 * Priority: URL path prefix (/th or /en) > HTML lang attribute > localStorage > default ('en')
 */
function getCurrentLanguage() {
    let lang = 'en';
    if (typeof window !== 'undefined' && window.location) {
        const path = window.location.pathname;
        if (path.startsWith('/th/') || path === '/th') {
            lang = 'th';
            try { localStorage.setItem('app_lang', 'th'); } catch(e) {}
            return 'th';
        } else if (path.startsWith('/en/') || path === '/en') {
            lang = 'en';
            try { localStorage.setItem('app_lang', 'en'); } catch(e) {}
            return 'en';
        }
    }
    if (typeof document !== 'undefined' && document.documentElement) {
        const docLang = document.documentElement.getAttribute('lang');
        if (docLang === 'th' || docLang === 'en') {
            return docLang;
        }
    }
    try {
        const saved = localStorage.getItem('app_lang');
        if (saved === 'th' || saved === 'en') return saved;
    } catch(e) {}
    return 'en';
}

/**
 * Apply translations to DOM elements
 */
function applyTranslations(lang) {
    if (!lang) lang = getCurrentLanguage();
    const dict = I18N_DICTIONARIES[lang] || I18N_DICTIONARIES['en'] || I18N_DICTIONARIES['th'];
    
    // Update document HTML lang attribute
    if (typeof document !== 'undefined' && document.documentElement) {
        document.documentElement.setAttribute('lang', lang);
    }
    
    // 1. Text elements: [data-i18n]
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    // 2. HTML elements: [data-i18n-html]
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
        const key = el.getAttribute('data-i18n-html');
        if (dict[key]) {
            el.innerHTML = dict[key];
        }
    });

    // 3. Placeholders: [data-i18n-placeholder]
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) {
            el.setAttribute('placeholder', dict[key]);
        }
    });

    // 4. Titles / Tooltips: [data-i18n-title]
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (dict[key]) {
            el.setAttribute('title', dict[key]);
        }
    });

    // Update Language Switcher Button UI
    updateLanguageButtonsUI(lang);

    // Dispatch custom event for dynamic components (e.g. charts, tables)
    window.dispatchEvent(new CustomEvent('appLanguageChanged', { detail: { lang } }));
}

/**
 * Update Language Switcher Buttons styling
 */
function updateLanguageButtonsUI(lang) {
    const btnTh = document.getElementById('langBtn-th');
    const btnEn = document.getElementById('langBtn-en');
    
    if (!btnTh || !btnEn) return;

    const activeClasses = ['bg-gradient-to-r', 'from-[#EA3815]', 'to-[#FF6B00]', 'text-white', 'shadow-md', 'font-black'];
    const inactiveClasses = ['text-stone-300', 'hover:text-amber-300', 'font-medium'];

    if (lang === 'en') {
        // EN Active
        btnEn.classList.add(...activeClasses);
        btnEn.classList.remove(...inactiveClasses);
        btnTh.classList.remove(...activeClasses);
        btnTh.classList.add(...inactiveClasses);
    } else {
        // TH Active
        btnTh.classList.add(...activeClasses);
        btnTh.classList.remove(...inactiveClasses);
        btnEn.classList.remove(...activeClasses);
        btnEn.classList.add(...inactiveClasses);
    }
}

/**
 * Change App Language, update URL path (/th <-> /en), and persist in localStorage
 */
function setAppLanguage(targetLang) {
    if (targetLang !== 'th' && targetLang !== 'en') targetLang = 'en';
    localStorage.setItem('app_lang', targetLang);

    if (typeof window !== 'undefined' && window.location) {
        const currentPath = window.location.pathname;
        let newPath = currentPath;

        if (currentPath.startsWith('/th/') || currentPath === '/th') {
            newPath = targetLang === 'en' ? currentPath.replace(/^\/th(\/|$)/, '/en$1') : currentPath;
        } else if (currentPath.startsWith('/en/') || currentPath === '/en') {
            newPath = targetLang === 'th' ? currentPath.replace(/^\/en(\/|$)/, '/th$1') : currentPath;
        } else {
            // Path didn't have /th or /en prefix (e.g. /paper or /)
            if (currentPath === '/') {
                newPath = `/${targetLang}`;
            } else {
                newPath = `/${targetLang}${currentPath}`;
            }
        }

        if (newPath !== currentPath) {
            window.location.href = newPath + window.location.search + window.location.hash;
            return;
        }
    }

    applyTranslations(targetLang);
}

// Expose globally
window.t = t;
window.getCurrentLanguage = getCurrentLanguage;
window.setAppLanguage = setAppLanguage;
window.applyTranslations = applyTranslations;

// Apply immediately if document exists
if (typeof document !== 'undefined' && document.documentElement) {
    const curLang = getCurrentLanguage();
    applyTranslations(curLang);
}

// And re-apply on DOM ready
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        const savedLang = getCurrentLanguage();
        applyTranslations(savedLang);
    });
}
