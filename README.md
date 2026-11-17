# 📄 Resume Reviewer on AWS

ระบบประเมินเรซูเม่ด้วย AI บน AWS 🤖
อัปโหลดเรซูเม่ (PDF) + วางประกาศงานที่สนใจ แล้วรับผลบนหน้าเว็บ ได้ทั้ง
คะแนนเรซูเม่ ความเข้ากันกับตำแหน่ง ทักษะที่ยังขาด และวิธีปรับเรซูเม่ให้ตรงกับงานนั้น

🎓 โปรเจกต์กลุ่มวิชา AWS, School of Information Technology and Innovation, Bangkok University
☁️ ทำงานบน AWS Learner Lab (region `us-east-1`)

---

## 🔗 ลิงก์สำหรับอาจารย์

| | รายการ | ลิงก์ |
|---|---|---|
| 🎬 | วิดีโอสาธิตการ implement | [https://drive.google.com/file/d/1LKyDtviYeb95ViPWp1owc6LD-1PX_PsR/view?usp=sharing] |
| 📘 | เอกสารขั้นตอนทำตาม | [https://canva.link/6ikov3iyme768ua] |
| 📑 | เอกสารขั้นตอนทำตาม PDF (สำรอง) | [https://drive.google.com/file/d/1KUWXdqMADkRQ8tjshCerMFzYhCFQeBbU/view?usp=sharing] |

---

## 💡 ประโยชน์ของแอป

คนหางานมักส่งเรซูเม่ฉบับเดียวไปหลายตำแหน่ง โดยไม่รู้ว่าตรงกับประกาศงานแค่ไหน
ระบบนี้ให้ฟีดแบ็กเป็นภาษาไทยภายในไม่กี่สิบวินาที:

- ⭐ **คะแนนเรซูเม่** ภาพรวม 0-100 พร้อมจุดแข็งและจุดที่ควรปรับ
- 🎯 **ความเข้ากันกับตำแหน่ง** เมื่อวางประกาศงาน (0-100)
- 🧩 **ทักษะที่ยังขาด** เทียบกับสิ่งที่ประกาศงานต้องการ
- ✍️ **วิธีปรับเรซูเม่** ให้ตรงกับตำแหน่งนั้น ๆ

### 💼 แนวทางต่อยอดเชิงธุรกิจ

- 👥 กลุ่มเป้าหมาย: นักศึกษาจบใหม่ ศูนย์จัดหางานของมหาวิทยาลัย บริษัทจัดหางาน/HR
- 💰 โมเดลรายได้ (ไอเดีย): ใช้ฟรีจำนวนครั้งจำกัดต่อเดือน แล้วเก็บรายเดือน หรือแพ็กเกจองค์กร

---

## ☁️ AWS services ที่ใช้

| | Service | หน้าที่ |
|---|---|---|
| 🪣 | Amazon S3 | เก็บเรซูเม่ (private) และโฮสต์หน้าเว็บ |
| 🌍 | Amazon CloudFront | แจกจ่ายหน้าเว็บผ่าน HTTPS |
| 🚪 | Amazon API Gateway | HTTP API ให้หน้าเว็บเรียก |
| ⚙️ | AWS Lambda | `ResumeAPI` รับ/ส่งผล และ `ResumeReviewer` เรียก Gemini |
| 🗄️ | Amazon DynamoDB | เก็บผลการประเมิน |
| 🔐 | IAM (LabRole), CloudWatch | สิทธิ์และ log (ไม่นับเป็น service หลัก) |

🤖 External API: Google Gemini API (อ่าน PDF และวิเคราะห์)

---

## 🗂️ แผนผังการวางไฟล์

📦 resume-reviewer-aws/
├── 📄 README.md                  ← ไฟล์นี้
├── 🙈 .gitignore
│
├── 📁 lambda/                    ← โค้ดฝั่งเซิร์ฟเวอร์ (Python 3.12)
│   ├── 🐍 processor_lambda.py    ← Lambda ResumeReviewer (S3 → Gemini → DynamoDB)
│   └── 🐍 api_lambda.py          ← Lambda ResumeAPI (อยู่หลัง API Gateway)
│
├── 📁 web/                       ← หน้าเว็บ
│   └── 🌐 index.html             ← ใส่ API URL ที่ตัวแปร API_URL ก่อนโฮสต์
│
└── 📁 docs/                      ← เอกสาร
    ├── 📘 DEPLOY.md              ← ขั้นตอนสร้างระบบตั้งแต่ต้น
    ├── 📑 slides.pdf             ← สไลด์ (เพิ่มเอง)
    └── 📁 screenshots/           ← ภาพหน้าจอประกอบ

### 🧭 ไฟล์ไหนไปอยู่ที่ไหนใน AWS

| ไฟล์ใน repo | นำไปวางที่ |
|---|---|
| 🐍 `lambda/processor_lambda.py` | Lambda function `ResumeReviewer` |
| 🐍 `lambda/api_lambda.py` | Lambda function `ResumeAPI` |
| 🌐 `web/index.html` | S3 bucket เว็บ (ผ่าน CloudFront) |

---

## ⚙️ การตั้งค่า (ไม่เก็บค่าจริงใน repo)

| Lambda | Environment variables | Memory / Timeout |
|---|---|---|
| `ResumeReviewer` | `TABLE_NAME`, `GEMINI_API_KEY`, `GEMINI_MODEL` (optional) | 512 MB / 2 นาที |
| `ResumeAPI` | `TABLE_NAME`, `BUCKET_NAME` | 128 MB / 30 วินาที |

---


## ⚠️ ข้อจำกัดที่ทราบ

- 📏 ไฟล์ PDF ไม่เกิน 4 MB (ข้อจำกัด payload ของ API Gateway/Lambda)
- 🔓 ยังไม่มีระบบล็อกอิน ผู้ที่ทราบรหัสผลลัพธ์เท่านั้นที่เปิดดูผลได้ ประวัติเก็บในเบราว์เซอร์ของแต่ละเครื่อง
- 🧠 ผลจาก AI เป็นคำแนะนำประกอบการตัดสินใจ ไม่ใช่การตัดสินแทนผู้สรรหา

## 🔒 ความปลอดภัย

- 🔑 ไม่เก็บ API key ใน repo (ใช้ Lambda environment variables)
- 🪣 bucket เก็บเรซูเม่เปิด Block all public access
- 🧪 ใช้เรซูเม่ตัวอย่างข้อมูลสมมติในการทดสอบและเดโม

---

## 👨‍👩‍👧‍👦 สมาชิกกลุ่ม

น.ส. กัญญาณัฐ สุดเชยชม  1660700947  
น.ส. กษิรา สาริมานนท์    1660701234 
น.ส. อาภรณ์ภัทร์ ปานช้าง  1660701473 
นาย จตุพร สุบิน          1660600188 
