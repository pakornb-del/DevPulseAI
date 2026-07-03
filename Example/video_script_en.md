# 🎬 คู่มือและสคริปต์การทำวิดีโอนำเสนอเพื่อส่งประกวด (World-Class YouTube Video Script)

คู่มือและสคริปต์ฉบับนี้จัดทำขึ้นสำหรับวิดีโอนำเสนอผลงานความยาวไม่เกิน 5 นาที เผยแพร่บน YouTube (Public) ตามเกณฑ์การตัดสิน **"วิดีโอนำเสนอผ่าน YouTube (10 คะแนน)"** ของ Kaggle

บทพากย์ถูกปรับให้เป็น **ภาษาพูดที่สละสลวย กระชับ ลื่นไหล เป็นธรรมชาติ** มีครบทั้ง **สคริปต์ภาษาอังกฤษ (สำหรับพากย์ AI/ใส่คำบรรยาย)** และ **สคริปต์ภาษาไทย (สำหรับอ่านพากย์เอง)** ครอบคลุมทั้ง 5 หัวข้อบังคับแยกเป็นหมวดหมู่อย่างชัดเจน

---

## 🎯 สรุปหัวข้อบังคับตามเกณฑ์การตัดสิน (Checklist 10 คะแนนเต็ม)

| #   | หัวข้อบังคับตามเกณฑ์ Kaggle                         | Segment   | เวลาพูด (EN/TH ประมาณ) |
| --- | --------------------------------------------------- | --------- | ---------------------- |
| 1   | นิยามปัญหา (Problem Definition)                     | ส่วนที่ 1 | ~40 วินาที             |
| 2   | เหตุผลที่เลือกเอเจนต์ (Why Agents)                  | ส่วนที่ 2 | ~25 วินาที             |
| 3   | สถาปัตยกรรมระบบ (Architecture)                      | ส่วนที่ 3 | ~20 วินาที             |
| 4   | ขั้นตอนการสร้างและเทคโนโลยี (Build Process & Tools) | ส่วนที่ 4 | ~40 วินาที             |
| 5   | วิดีโอสาธิตการทำงานจริง (Live Demo)                 | ส่วนที่ 5 | ~55 วินาที             |

---

## 🛠️ เครื่องมือสร้างวิดีโอแนะนำ (ฟรี 100%)

1. **บันทึกหน้าจอ (Screen Recording)**:
   - Windows 10/11 กดปุ่ม `Win + Alt + R` หรือใช้ **OBS Studio** / **Loom.com**
2. **แปลงข้อความเป็นเสียงพากย์ AI (Text-to-Speech)**:
   - **Windows Clipchamp** (มีแถมใน Windows 11): คัดลอก **English Audio Script** แล้ววางได้เลย ได้เสียง AI ระดับพรีเมียมฟรีทันที
   - หากต้องการพากย์เสียงไทย ใช้น้ำเสียง TH ใน Clipchamp หรืออ่านเองจาก **Thai Audio Script**

> **หมายเหตุสำหรับตัดต่อ**: ไฟล์ภาพประกอบทั้งหมดอยู่ในโฟลเดอร์ `document/` ของโปรเจกต์ และไฟล์สัญญาตัวอย่างอยู่ใน `test_documents/`

---

## ⏱️ บทพากย์แบ่งตามช่วงเวลา (รวมประมาณ 3:30–4:00 นาที)

---

### 🎬 ส่วนที่ 1 — นิยามปัญหาและความเหลื่อมล้ำ (Problem Definition) [0:00–0:45]

**หัวข้อตามเกณฑ์**: ✅ นิยามปัญหา (Problem Definition)

**Visual Timeline**:
| เวลา | สิ่งที่แสดงบนหน้าจอ |
|---|---|
| 0:00–0:12 | สไลด์เปิดตัว: โลโก้ + ชื่อโครงการ **ThaiAgriLease: AI for Agricultural Justice** |
| 0:12–0:28 | `document/lease_contract_doc.png` — ภาพสัญญาเช่านาที่ไม่เป็นธรรม |
| 0:28–0:45 | `document/disaster_rice_field.png` — ภาพภัยธรรมชาติและแปลงนาเสียหาย |

**🎙️ English Audio Script** (~40 วินาที):
> "In Thailand, nearly 30% of farming households do not own agricultural land—rising above 40% in major rice-producing provinces. Bound by legal illiteracy and severe information asymmetry, farmers frequently sign exploitative leases that violate statutory six-year protections and erase inheritance rights. When natural disasters strike, landlords often demand full rent, ignoring mandatory relief under Section 43. This is why we built ThaiAgriLease: an intelligent AI agent platform designed to protect farmer rights and restore agricultural justice."

**🎙️ สคริปต์พากย์ไทย** (~40 วินาที):
> "ในประเทศไทย ครัวเรือนเกษตรกรเกือบ 30% ไม่มีที่ดินทำกินเป็นของตนเอง และสถิตินี้พุ่งสูงกว่า 40% ในพื้นที่ทำนาหลัก ด้วยความเหลื่อมล้ำทางข้อมูลและความรู้กฎหมาย ชาวนาจำนวนมากจำต้องเซ็นสัญญาเช่าที่ไม่เป็นธรรม ถูกเอาเปรียบเรื่องระยะเวลา สิทธิมรดก และเสี่ยงถูกบอกเลิกสัญญาโดยมิชอบ ยิ่งเมื่อเกิดภัยธรรมชาติ เจ้าของที่ดินมักเรียกเก็บค่าเช่าเต็มจำนวน โดยมองข้ามสิทธิลดหย่อนตามมาตรา 43 นี่คือเหตุผลที่เราพัฒนา ThaiAgriLease — แพลตฟอร์ม AI Agent เพื่อปกป้องสิทธิ์และสร้างความเป็นธรรมให้เกษตรกรไทย"

---

### 🤖 ส่วนที่ 2 — ทำไมต้องใช้ AI Agent (Why Agents) [0:45–1:10]

**หัวข้อตามเกณฑ์**: ✅ เหตุผลที่เลือกเอเจนต์ (Why Agents)

**Visual Timeline**:
| เวลา | สิ่งที่แสดงบนหน้าจอ |
|---|---|
| 0:45–1:10 | สไลด์เปรียบเทียบ: Traditional Software vs LLM vs AI Agent (ข้อจำกัดและทางออก) |

**🎙️ English Audio Script** (~25 วินาที):
> "Why AI Agents? Traditional software cannot parse complex legal language. Standard LLMs risk hallucinations and math errors on critical calculations. Agents solve this by combining legal reasoning, verified tool calls, and local Python math into a single autonomous workflow—giving farmers reliable, accurate results every time."

**🎙️ สคริปต์พากย์ไทย** (~25 วินาที):
> "ทำไมต้องใช้ AI Agent? เพราะซอฟต์แวร์แบบเดิมวิเคราะห์ภาษากฎหมายที่ซับซ้อนไม่ได้ และโมเดล LLM ทั่วไปเสี่ยงคำนวณผิดหรือสร้างข้อมูลมโน AI Agent แก้ปัญหานี้ด้วยการผสานการให้เหตุผลทางกฎหมาย, การเรียกใช้เครื่องมือที่ตรวจสอบแล้ว และการคำนวณ Python ในเครื่อง เพื่อให้ผลลัพธ์ที่แม่นยำและเชื่อถือได้"

---

### 🏗️ ส่วนที่ 3 — สถาปัตยกรรมระบบ (Architecture) [1:10–1:30]

**หัวข้อตามเกณฑ์**: ✅ สถาปัตยกรรม (Architecture)

**Visual Timeline**:
| เวลา | สิ่งที่แสดงบนหน้าจอ |
|---|---|
| 1:10–1:30 | Mermaid Architecture Diagram: แสดง LeaseAuditor → 4 Skills → FastMCP → Legal DB + Python Engine |

**🎙️ English Audio Script** (~20 วินาที):
> "Our core agent, LeaseAuditor, built on Google ADK 2.0, integrates four specialized skills: document validation, six-clause compliance auditing, disaster relief calculations, and legal advocacy drafting. Connected via Model Context Protocol to verified legal databases, it delivers fast, hallucination-resistant results."

**🎙️ สคริปต์พากย์ไทย** (~20 วินาที):
> "เอเจนต์หลัก LeaseAuditor บน Google ADK 2.0 รวม 4 ทักษะเชี่ยวชาญ ได้แก่ การคัดแยกเอกสาร, ตรวจสอบกฎหมาย 6 มาตรา, คำนวณภัยพิบัติ และร่างหนังสือยื่นสิทธิ์ เชื่อมต่อผ่าน FastMCP กับฐานข้อมูลกฎหมาย เพื่อผลลัพธ์รวดเร็วและป้องกันการมโนทางกฎหมาย"

---

### 🛠️ ส่วนที่ 4 — ขั้นตอนการสร้างและเทคโนโลยี (Build Process & Tools) [1:30–2:10]

**หัวข้อตามเกณฑ์**: ✅ ขั้นตอนการสร้างและเทคโนโลยี (Build Process & Tools)

**Visual Timeline**:
| เวลา | สิ่งที่แสดงบนหน้าจอ |
|---|---|
| 1:30–1:50 | Terminal: รัน `uv run pytest` → ผลลัพธ์ **11 passed** สีเขียว |
| 1:50–2:10 | หน้าต่างโค้ด + Antigravity AI Assistant + รัน `uv run python main.py` |

> 💡 **เทคนิคการถ่ายทำและคำสั่งตัวอย่างสำหรับ Antigravity AI Assistant (ผสมผสาน 3 แนวทางเซฟโค้ด 100%):**
> 1. **แนวทางที่ 1 (สั่งให้สรุป/อธิบาย - Read-only):** พิมพ์คำถามเพื่อให้ AI อธิบายโดยไม่แก้โค้ด เช่น
>    - `"ช่วยสรุปสถาปัตยกรรมของ LeaseAuditor Agent และความเชื่อมโยงกับทั้ง 4 Skills ในโปรเจกต์นี้ให้หน่อย"`
>    - `"ช่วยตรวจสอบว่าในโปรเจกต์นี้ เรามีระบบปกป้องความเป็นส่วนตัว (PII Masking) ของเกษตรกรตรงจุดไหนบ้าง"`
>    - `"สรุปรายการ Unit & Integration Tests ทั้งหมดในโฟลเดอร์ tests/ ให้หน่อยว่าครอบคลุมการทดสอบอะไรบ้าง"`
> 2. **แนวทางที่ 2 (ถามเตรียมความพร้อมรันระบบ):** พิมพ์คำถามสั้นๆ เช่น
>    - `"โปรเจกต์ ThaiAgriLease พร้อมรันรึยัง? ขอคำสั่งในการสตาร์ทเซิร์ฟเวอร์ด้วย uv หน่อย"`
> 3. **แนวทางที่ 3 (โชว์ประวัติแชทเดิม):** เลื่อน Scroll หน้าต่างแชท Antigravity ค้างไว้ที่ประวัติการช่วยพัฒนาเดิมที่ดูสวยงาม
> 🎬 **ลำดับการอัดช่วง 1:50–2:10:** เลื่อนดูแชทเดิม/พิมพ์คำถามอธิบาย ให้ AI เจนคำตอบสวยๆ แล้วย้ายมา Terminal ด้านล่างรัน `uv run python main.py` เพื่อสตาร์ทเซิร์ฟเวอร์
### 🎬 ลำดับขั้นตอนการอัดช่วง 1:50–2:10 ให้ได้ภาพสวยงาม

1. **[ใน Terminal]** พิมพ์รัน `uv run pytest` → ผลลัพธ์ขึ้นเขียว **11 passed** (ใช้เวลา 1:30–1:50)
2. **[หน้าต่าง Antigravity]** พิมพ์คำถามตามตัวอย่างด้านบน (เช่น _"ช่วยสรุปสถาปัตยกรรมของ LeaseAuditor Agent..."_) แล้วกดส่ง ให้เห็น AI กำลังเจนข้อความสรุปสวยๆ ออกมา
3. **[ใน Terminal]** พิมพ์รัน `uv run python main.py` แล้วกด Enter ให้เห็นข้อความ Uvicorn/FastAPI สตาร์ทขึ้นมาเป็นอันเสร็จสิ้นช่วงนี้ครับ!


**🎙️ English Audio Script** (~40 วินาที):
> "We built this system alongside the Antigravity AI coding assistant, which helped us architect modular skills, enforce local PII scrubbing to protect farmer privacy, and craft automated test suites. The entire application is packaged with Astral 'uv' for streamlined deployment. To guarantee high uptime, we engineered an automated three-model fallback client transitioning across Gemini 2.5 Flash, 2.0 Flash, and Flash Lite upon hitting API quotas. Running our test suite confirms the end-to-end pipeline passes all 11 unit and integration tests."

**🎙️ สคริปต์พากย์ไทย** (~40 วินาที):
> "เราพัฒนาระบบนี้ร่วมกับ Antigravity AI Assistant ที่ช่วยออกแบบสถาปัตยกรรมทักษะเอเจนต์ ระบบปกป้อง PII ของชาวนา และชุดทดสอบอัตโนมัติ ทั้งหมดถูกจัดแพ็กเกจด้วย Astral 'uv' เพื่อการติดตั้งที่สะดวก นอกจากนี้เราสร้างระบบ Fallback สลับ 3 โมเดลอัตโนมัติ ได้แก่ Gemini 2.5 Flash, 2.0 Flash และ Flash Lite เมื่อชนโควตา API การรันคำสั่ง `uv run pytest` ยืนยันความสมบูรณ์ของระบบด้วยการทดสอบผ่านครบ 11 รายการ"

---

### 💻 ส่วนที่ 5 — สาธิตการใช้งานจริง (Live Demo) [2:10–3:05]

**หัวข้อตามเกณฑ์**: ✅ วิดีโอสาธิต (Live Demo)

**Visual Timeline**:
| เวลา | สิ่งที่แสดงบนหน้าจอ |
|---|---|
| 2:10 | เปิดบราวเซอร์ `http://127.0.0.1:8000` |
| 2:15 | ลากไฟล์ `test_documents/violating_lease_contract.pdf` อัปโหลดเข้าระบบ |
| 2:25 | เลือกจังหวัด, ชนิดพืช, กรอกตัวเลขผลผลิตจริง |
| 2:35 | กดปุ่มตรวจสอบ |
| 2:40–3:05 | เลื่อนแสดงผลรายงาน: ตารางจับผิดกฎหมาย → ตัวเลขภัยพิบัติมาตรา 43 → หนังสือยื่นสู้สิทธิ์ |

**🎙️ English Audio Script** (~55 วินาที):
> "Here is ThaiAgriLease in action through our web portal, designed for farmers with no technical background. The user simply uploads their lease contract. Local regex engines immediately mask national IDs and phone numbers to guarantee privacy. After entering crop yield damage parameters, our agent audits the agreement in seconds—delivering a crystal-clear legal evaluation table flagging every violation, Section 43 rent waiver calculations, and formal print-ready demand letters that farmers can sign and submit immediately to defend their rights."

**🎙️ สคริปต์พากย์ไทย** (~55 วินาที):
> "นี่คือการทำงานจริงของ ThaiAgriLease บนเว็บพอร์ทัลภาษาไทยที่ออกแบบมาเพื่อเกษตรกร ชาวนาเพียงอัปโหลดไฟล์สัญญาเช่า ระบบจะลบเลขบัตรประชาชนและเบอร์โทรศัพท์ออกทันทีเพื่อความปลอดภัย เมื่อกรอกข้อมูลความเสียหายจากภัยพิบัติ เอเจนต์วิเคราะห์สัญญาเสร็จในไม่กี่วินาที โดยแสดงตารางประเมินกฎหมายที่แม่นยำ สรุปยอดลดหย่อนค่าเช่าตามมาตรา 43 และหนังสือยื่นสู้สิทธิ์ที่เป็นทางการ ซึ่งชาวนาสามารถปริ้นท์ เซ็นชื่อ และยื่นเรื่องได้ทันที"

---

### 🤝 ส่วนที่ 6 — สรุปวิสัยทัศน์และผลกระทบ (Impact & Vision) [3:05–3:35]

**หัวข้อตามเกณฑ์**: สรุปคุณค่าและเป้าหมายโครงการ

**Visual Timeline**:
| เวลา | สิ่งที่แสดงบนหน้าจอ |
|---|---|
| 3:05–3:30 | สไลด์ Impact: ตัวเลขและผลลัพธ์ที่คาดหวัง |
| 3:30–3:35 | `document/thank_you_slide.png` — สไลด์ปิดท้าย แช่จนจบวิดีโอ |

**🎙️ English Audio Script** (~30 วินาที):
> "By bridging the legal literacy gap with agentic AI, ThaiAgriLease turns complex legislation into actionable protection—securing land rights and statutory disaster relief for smallholder farmers across Thailand. Technology is at its most powerful when it protects the most vulnerable. Thank you for watching, and let's build agricultural justice together."

**🎙️ สคริปต์พากย์ไทย** (~30 วินาที):
> "ด้วยการเชื่อมช่องว่างทางกฎหมายด้วย Agentic AI, ThaiAgriLease เปลี่ยนข้อกฎหมายที่ซับซ้อนให้กลายเป็นการคุ้มครองที่จับต้องได้ เพื่อปกป้องสิทธิ์ที่ดินทำกินและความคุ้มครองจากภัยธรรมชาติให้เกษตรกรรายย่อยทั่วไทย เทคโนโลยีจะมีความหมายที่สุดเมื่อถูกใช้เพื่อผู้ที่ต้องการความช่วยเหลือ ขอบคุณทุกท่านที่รับชม มาร่วมสร้างความเป็นธรรมทางการเกษตรไปด้วยกันครับ"

---

## 💡 ตัวหนังสือคำบรรยายบนหน้าจอ (Screen Text Captions)

ใส่ text overlay บนสไลด์วิดีโอเพื่อเน้นประเด็นหลัก:

| # | Caption |
|---|---|
| 1 | **Problem**: "Nearly 30% of Thai farmers rely on rented land, facing severe legal illiteracy." |
| 2 | **Why Agents**: "AI Agents combine legal reasoning + verified tools + local math—no hallucinations." |
| 3 | **Architecture**: "ADK 2.0 + FastMCP: LeaseAuditor with 4 Specialized Skills." |
| 4 | **Tools & Build**: "Antigravity AI + Astral uv + 3-Model Fallback Engine. All 11 tests passed." |
| 5 | **Live Demo**: "Instant legal audit · Section 43 rent waivers · Print-ready advocacy letters." |
| 6 | **Impact**: "Bridging the legal gap to protect smallholder farmer rights across Thailand." |
