# 🧾 Comprehensive Implementation Plan: Smart Receipt & Expense Agent (Handwritten & Printed Real-World Receipts)

แผนการดำเนินงานฉบับสมบูรณ์เชิงลึกสำหรับการพัฒนา **Smart Receipt & Expense Agent** ระบบเอเจนต์ AI ผู้ช่วยสกัดข้อมูล ตรวจสอบ และสรุปรายงานเบิกจ่ายอัจฉริยะ สำหรับส่งแข่งขันในโครงการ **AI Agents: Intensive Vibe Coding Capstone Project (หมวด Agents for Business)** 

แผนงานนี้ถูกออกแบบมาเพื่อรองรับ **"ใบเสร็จในชีวิตจริง (Real-world Receipts)"** ทุกรูปแบบ ทั้งเอกสารพิมพ์ดิจิทัล เอกสารใบเสร็จจากเครื่องรับเงินสด และ **ใบเสร็จเขียนมือ (Handwritten Receipts)** ซึ่งมีความท้าทายเรื่องความคมชัด ตัวเลข ลายมือ ลายเซ็น และรอยพับ/รอยย่นของกระดาษ

---

## 📌 User Review Required & Design Principles

> [!IMPORTANT]
> **การรับมือใบเสร็จเขียนมือ (Handwritten & Low-Quality Receipts Strategy):**
> 1. **Multimodal LLM Capability:** เลือกใช้ **Gemini 2.5 Flash** ซึ่งมี Vision Capabilities ประสิทธิภาพสูงในการอ่านภาษาไทยและตัวเลขเขียนมือ
> 2. **Preflight Document Validation & Confidence Score:** เพิ่มระบบตรวจเช็กสภาพเอกสารก่อนประมวลผล หากรูปภาพมืดเกินไป รอยย่นบังข้อความ หรือตัวเลขเขียนมืออ่านยาก ระบบจะคืนค่า **Confidence Score** และอนุญาตให้ผู้ใช้กดยืนยัน/แก้ไขตัวเลขบนหน้าเว็บได้ทันที เพื่อป้องกันข้อผิดพลาดทางบัญชี 100%

> [!NOTE]
> **สถาปัตยกรรมระบบการจัดการ Session (Persistent Session Storage):**
> จัดเก็บข้อมูล Session ลงใน **SQLite Database (`app/sessions.db`)** เพื่อให้ข้อมูลรอบการเบิกจ่าย (Expense Claim Sessions) ไม่สูญหายเมื่อรีสตาร์ทเซิร์ฟเวอร์ และรองรับการสลับไปมาระหว่างหลายๆ เซสชันของผู้ใช้

---

## 🏗️ Complete Project Directory Structure

```text
smart-receipt-agent/
├── .agents/
│   └── skills/                         # 💡 4 Modular Agent Skills (.agents/skills/)
│       ├── document-preflight-validation/
│       │   └── SKILL.md                # Skill 0: ตรวจชนิดเอกสาร ความคมชัด และจำแนก (พิมพ์/เขียนมือ)
│       ├── receipt-ocr-parser/
│       │   └── SKILL.md                # Skill 1: สกัดข้อมูลภาพถ่ายใบเสร็จ (Printed & Handwritten Prompting)
│       ├── policy-compliance-audit/
│       │   └── SKILL.md                # Skill 2: กฎและเพดานงบประมาณการเบิกจ่ายตามนโยบายบริษัท
│       └── expense-report-generator/
│           └── SKILL.md                # Skill 3: จัดโครงสร้างตารางสรุปรายงานและคำนวณภาษีมูลค่าเพิ่ม (VAT 7%)
├── app/
│   ├── __init__.py
│   ├── agent.py                        # ADK 2.0 Multi-Agent Orchestrator & State Graph
│   ├── session_manager.py              # SQLite Persistent Session & History State Engine
│   ├── security.py                     # Regular Expression PII Scrubbing Engine (บัตร/เบอร์/เบอร์บัญชี)
│   └── utils.py                        # Helper functions (Image resizing, Base64 encoding)
├── database/
│   ├── budget_policies.json            # เพดานงบประมาณและนโยบายการเบิกจ่าย (สำหรับ MCP)
│   └── sessions.db                     # SQLite Database สำหรับเซสชันและความจำของเอเจนต์
├── mcp_server.py                       # FastMCP Server เผยแพร่ Tools ให้ LLM เรียกใช้
├── main.py                             # Web Dashboard Portal (Streamlit หรือ FastAPI Dashboard)
├── test_documents/                     # ชุดรูปภาพใบเสร็จจริงสำหรับการทดสอบ (Test Dataset)
│   ├── printed_receipt_01.jpg
│   ├── handwritten_receipt_01.jpg
│   └── low_quality_receipt.jpg
├── tests/                              # ชุดทดสอบอัตโนมัติ (Pytest Integration & Unit Tests)
│   ├── test_security.py
│   ├── test_mcp.py
│   ├── test_session.py
│   └── test_agent_workflow.py
├── README.md                           # เอกสารโครงการฉบับสมบูรณ์ (อัปขึ้น GitHub)
└── pyproject.toml                      # การตั้งค่า dependencies ด้วย uv
```

---

## 🛠️ Detailed Component Implementation Plan

---

### Phase 1: Modular Agent Skills (`.agents/skills/`)

ออกแบบ Skills 4 ตัวเพื่อแบ่งหน้าที่การประมวลผลเอกสารอย่างเป็นระบบ:

#### 1. [NEW] [.agents/skills/document-preflight-validation/SKILL.md](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/.agents/skills/document-preflight-validation/SKILL.md)
* **เป้าหมาย:** ตรวจสอบก่อนเริ่มสกัดข้อมูล (Preflight Checks)
* **การทำงาน:**
  * ตรวจสอบว่าภาพอัปโหลดเป็นเอกสารการเงินจริงหรือไม่ (ใช่/ไม่ใช่)
  * จำแนกประเภทเอกสาร: `PRINTED_TAX_INVOICE`, `HANDWRITTEN_RECEIPT`, หรือ `NON_RECEIPT`
  * ประเมินความชัดเจนของภาพ (Blurriness / Lighting) และให้ค่า `quality_score` (0.0 - 1.0)

#### 2. [NEW] [.agents/skills/receipt-ocr-parser/SKILL.md](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/.agents/skills/receipt-ocr-parser/SKILL.md)
* **เป้าหมาย:** สกัดข้อมูลโครงสร้าง JSON จากภาพใบเสร็จพิมพ์และเขียนมือ
* **การทำงาน:**
  * Prompting พิเศษสำหรับอ่านลายมือภาษาไทยและตัวเลขเขียนมือ (เช่น เลข ๑-๙ หรือตัวเลขไทย/อารบิก)
  * สกัด ฟิลด์ข้อมูล: `merchant_name`, `tax_id` (13 หลัก), `date`, `items_list`, `subtotal`, `vat_7%`, `total_amount`
  * ให้ค่า `confidence_score` รายฟิลด์ โดยเฉพาะฟิลด์ยอดเงินรวม

#### 3. [NEW] [.agents/skills/policy-compliance-audit/SKILL.md](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/.agents/skills/policy-compliance-audit/SKILL.md)
* **เป้าหมาย:** ตรวจสอบความถูกต้องตามนโยบายงบประมาณบริษัท
* **การทำงาน:**
  * เปรียบเทียบยอดเงินกับเพดานงบประมาณ (สืบค้นผ่าน MCP Server)
  * ตรวจสอบความสมบูรณ์ของใบเสร็จเขียนมือ (ใบเสร็จเขียนมือต้องมีชื่อ-ที่อยู่ผู้รับเงิน และลายเซ็นผู้รับเงิน)

#### 4. [NEW] [.agents/skills/expense-report-generator/SKILL.md](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/.agents/skills/expense-report-generator/SKILL.md)
* **เป้าหมาย:** สร้างสรุปรายงานผลการตรวจสอบประจำ Session
* **การทำงาน:** จัดกลุ่มใบเสร็จแยกตามหมวดหมู่ คำนวณภาษีซื้อถอนคืนได้ (Claimable VAT) และสร้างบทสรุปข้อเตือนใจสำหรับการอนุมัติเบิกจ่าย

---

### Phase 2: Knowledge Base & FastMCP Server (`database/` & `mcp_server.py`)

#### 1. [NEW] [database/budget_policies.json](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/database/budget_policies.json)
* จัดเก็บฐานข้อมูลเพดานงบประมาณและเงื่อนไขทางกฎหมาย เช่น:
  * `FOOD_AND_BEVERAGE`: เพดาน 500 บาท/คน/วัน (ไม่ต้องมีใบกำกับภาษีเต็มรูป)
  * `FUEL_AND_TRANSPORT`: เพดาน 3,000 บาท/เที่ยว (ต้องมี Tax ID 13 หลัก)
  * `HANDWRITTEN_LIMIT`: ใบเสร็จเขียนมือยอมรับยอดเงินไม่เกิน 1,500 บาท/ฉบับ

#### 2. [NEW] [mcp_server.py](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/mcp_server.py)
* พัฒนาเซิร์ฟเวอร์ด้วย `FastMCP` สร้าง Tools ดังนี้:
  * `@mcp.tool() def query_budget_policy(category: str) -> dict`: คืนค่าเพดานงบและเงื่อนไขตามหมวดหมู่
  * `@mcp.tool() def verify_thai_tax_id(tax_id: str) -> dict`: ตรวจสอบความถูกต้องของโครงสร้างเลขประจำตัวผู้เสียภาษี 13 หลักตามอัลกอริทึม Checksum
  * `@mcp.tool() def get_handwritten_receipt_rules() -> dict`: คืนค่ากฎระเบียบเฉพาะสำหรับใบเสร็จเขียนมือ

---

### Phase 3: Core Logic, Security & Persistent Sessions (`app/`)

#### 1. [NEW] [app/security.py](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/app/security.py)
* ฟังก์ชัน `scrub_pii_data(text_or_metadata: str/dict) -> dict`:
  * ตรวจจับและทำความสะอาด (Masking) เลขบัตรเครดิต/เดบิต (16 หลัก) -> `XXXX-XXXX-XXXX-1234`
  * ทำความสะอาดเลขบัญชีธนาคารส่วนตัวและเบอร์โทรศัพท์ก่อนส่งให้ LLM หรือแสดงบนหน้าเว็บ

#### 2. [NEW] [app/session_manager.py](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/app/session_manager.py)
* จัดการฐานข้อมูล SQLite (`database/sessions.db`) โครงสร้างตาราง:
  * `sessions`: `session_id`, `title`, `created_at`, `total_accumulated_amount`, `status`
  * `receipts`: `receipt_id`, `session_id`, `image_path`, `merchant_name`, `total_amount`, `confidence`, `is_handwritten`, `audit_status`
  * `chat_history`: `message_id`, `session_id`, `sender` (user/agent), `message_text`, `timestamp`
* มีเมธอดรองรับการสร้างเซสชัน เพิ่มใบเสร็จสะสม อัปเดตข้อมูลแก้ไขจากผู้ใช้ และดึงประวัติมาแสดงผล

#### 3. [NEW] [app/agent.py](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/app/agent.py)
* พัฒนาสถาปัตยกรรม Multi-Agent Graph (ADK 2.0 Engine):
  * **Step 1:** Preflight Agent รัน Skill `document-preflight-validation`
  * **Step 2:** OCR Agent รัน Skill `receipt-ocr-parser` อ่านข้อมูลภาพ
  * **Step 3:** PII Sanitizer เรียกใช้ `security.py` กรองข้อมูล
  * **Step 4:** Audit Agent เรียกใช้ MCP Server และ Skill `policy-compliance-audit` ตรวจสอบกฎ
  * **Step 5:** Session Synchronizer บันทึกผลลัพธ์ลง `session_manager.py`

---

### Phase 4: Web Application Portal & Automated Testing (`main.py` & `tests/`)

#### 1. [NEW] [main.py](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/main.py)
* สร้าง Web Interface ด้วย Streamlit หรือ FastAPI Dashboard ที่มีฟีเจอร์เด่น:
  * **Interactive Receipt Inspector:** หากใบเสร็จเป็น **แบบเขียนมือ (Handwritten)** หรือมีค่า `confidence_score < 0.8` ระบบจะขึ้นกรอบสีเหลืองเพื่อให้ผู้ใช้อ่านภาพเปรียบเทียบและกดแก้ไขตัวเลขได้ทันทีก่อนบันทึก
  * **Batch Claiming Dashboard:** แสดงการสะสมใบเสร็จใน Session เดียวกันพร้อมยอดรวมเงินสะสมเรียลไทม์
  * **Agent Chat Assistant:** ช่องทางพูดคุยซักถามเหตุผลการไม่อนุมัติเบิกจ่ายกับ Agent

#### 2. [NEW] [tests/](file:///c:/Users/Dell/Desktop/ProjectAgent/5_day_ai_agents/smart-receipt-agent/tests/)
* เขียนไฟล์ทดสอบให้ครบ 100%:
  * `test_security.py`: ทดสอบ Regex PII Masking
  * `test_mcp.py`: ทดสอบ FastMCP Server Tool Execution
  * `test_session.py`: ทดสอบ SQLite Session Storage persistence
  * `test_agent_workflow.py`: ทดสอบ End-to-End Workflow ร่วมกับไฟล์ตัวอย่างใน `test_documents/`

---

## 🧪 Detailed Verification & Validation Plan

### Automated Testing Suite (`uv run pytest`)
1. **Unit Test - Security PII Scrubbing:** ทดสอบส่งสตริงที่มีเลขบัตรเครดิตและเบอร์โทรศัพท์ ให้ผลลัพธ์ผ่านการเซ็นเซอร์ถูกต้อง
2. **Unit Test - FastMCP Integrity:** ทดสอบดึงข้อมูลเพดานงบประมาณผ่าน MCP Tools ได้ค่าตรงตาม `budget_policies.json`
3. **Integration Test - Handwritten Receipt Parsing:** ทดสอบส่งรูปภาพ `handwritten_receipt_01.jpg` เข้า Workflow สกัดข้อมูลและประเมินค่า Confidence สอดคล้องตามเกณฑ์

### Manual Verification & Demo Flow (สำหรับวิดีโอ 5 นาที)
1. **ทดสอบใบเสร็จพิมพ์ดิจิทัลปกติ:** อัปโหลดใบเสร็จสแกน QR Code / เซเว่น / ปั๊มน้ำมัน ตรวจสอบการอ่านค่าแม่นยำ 100%
2. **ทดสอบใบเสร็จเขียนมือ (Handwritten Test):** อัปโหลดรูปภาพใบเสร็จเขียนมือที่มีลายเซ็นผู้รับเงิน ตรวจสอบว่าระบบจำแนกประเภทเป็น `HANDWRITTEN_RECEIPT` และแสดงกรอบให้ผู้ใช้ช่วยยืนยันตัวเลขบน Web UI
3. **ทดสอบ Session & Conversational Agent:** อัปโหลดใบเสร็จเพิ่มเข้า Session ใบที่ 2 และ 3 จากนั้นพิมพ์ถาม Agent ในช่องแชตว่า *"ใบเสร็จใบไหนที่มีปัญหาผิดกฎบริษัทบ้าง"* ตรวจสอบว่า Agent ตอบคำถามโดยอ้างอิง Context ของเซสชันได้อย่างถูกต้อง
