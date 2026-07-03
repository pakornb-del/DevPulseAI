# 🧾 Comprehensive Implementation Plan: Excel Roadmap Chatbot Agent (Google Sheets & Drive Integration)

แผนการดำเนินงานและสถาปัตยกรรมระดับลึกสำหรับการพัฒนา **Excel Roadmap Chatbot Agent** ระบบเอเจนต์ผู้ช่วยติดตาม วิเคราะห์แผนงาน และจัดสรรงานอัจฉริยะจาก Google Sheets ทั้งสิ้น 7 ไฟล์ บน Google Drive สำหรับส่งประกวดผลงาน **AI Agents: Intensive Vibe Coding Capstone Project (หมวด Agents for Business)**

แผนงานนี้อ้างอิงโครงสร้างฐานข้อมูลตารางแบบไฮบริด (Hybrid Table Database) ซึ่งประกอบด้วยชีตสรุปภาพรวม (`Project`) และชีตรายละเอียดงานย่อยของแต่ละโครงการ (`ST1`, `ST2`, `ST3`, ...) แยกย่อยรายโครงการ

---

## 📌 User Review Required & Design Principles

> [!IMPORTANT]
> **โครงสร้างและการสืบค้นชีตย่อยแบบสองระดับ (Two-Level Sheets Query Strategy):**
> 1. **Macro Query (ใช้ชีต Project):** เมื่อคำสั่งถามเกี่ยวกับภาพรวมทีม ความคืบหน้าโครงการรายระบบ หรือกำหนดส่งงาน (เช่น *"ระบบบรรจุคืบหน้าไปกี่เปอร์เซ็นต์"*) เอเจนต์จะสืบค้นผ่านชีต `Project` โดยดึงฟิลด์ในคอลัมน์ B (รหัสโครงการ), C (ชื่อระบบ), N (ความคืบหน้า %), และ J (กำหนดส่งงาน) มาประมวลผลทันทีเพื่อประหยัดเวลาและพลังงาน Token
> 2. **Micro Query (ใช้ชีต ST*):** เมื่อคำสั่งเจาะลึกงานย่อยหรือการติดตามงานบุคคล (เช่น *"พีทกำลังทำอะไรอยู่"*, *"คิวกำลังพัฒนางาน Doing อะไรในระบบบรรจุ"*) เอเจนต์จะทำการสแกนเฉพาะชีตที่มีชื่อขึ้นต้นด้วย `ST` (เช่น `ST1`, `ST2`) เพื่อเข้าไปเช็กรายชื่องานย่อย, ผู้รับผิดชอบ และสถานะของงานย่อยนั้นๆ (To Do / Doing / Done)

> [!NOTE]
> **การรับมือปัญหาสิทธิ์เข้าถึงไฟล์ Google Sheets ของทั้ง 7 ทีม:**
> ดึงข้อมูลผ่าน **Google Service Account** โดยแชร์ลิงก์ Google Sheets ทั้ง 7 ไฟล์ให้กับอีเมลของ Service Account (เช่น `agent-service@project.iam.gserviceaccount.com`) เป็นสิทธิ์ Viewer/Editor ทำให้ AI เข้าถึงไฟล์แบบคลาวด์ได้แบบ Real-time โดยไม่ต้องผ่านหน้าต่างล็อกอินของ OAuth ทุกครั้งที่รันการทดสอบ

---

## 🎓 Alignment with Capstone Project Criteria (การตอบโจทย์เกณฑ์ Capstone Project)

ระบบนี้ถูกออกแบบมาเพื่อส่งมอบผลงานที่ตรงตามเกณฑ์หลักของ Kaggle / Google Capstone Project ครบทั้ง **6 ข้อ** ดังนี้:

| แนวคิดหลัก (Key Concept) | การตอบโจทย์ในระบบนี้ (How it is met) | จุดแสดงผลงาน (Where to Demonstrate) | คำแนะนำเพิ่มเติมเพื่อให้ได้คะแนนเต็ม |
| :--- | :--- | :--- | :--- |
| **1. ระบบเอเจนต์ / มัลติเอเจนต์ (ADK)** | พัฒนา Multi-Agent Orchestrator ใน `app/agent.py` แบ่งภารกิจประสานงานระหว่าง เอเจนต์อ่านข้อมูลชีต, เอเจนต์คํานวณสถิติ, เอเจนต์วิเคราะห์ทรัพยากรบุคคล (Resource Optimization) และเอเจนต์แจ้งเตือนความเสี่ยง | รหัสโค้ด (Code) | เขียนคอมเมนต์อธิบายวงจรรูปแบบ State Graph และการทำงานร่วมกันของเอเจนต์ในไฟล์โค้ดให้อ่านง่าย |
| **2. เซิร์ฟเวอร์ MCP (MCP Server)** | สร้างเซิร์ฟเวอร์ MCP ใน `mcp_server.py` โดยลงทะเบียน Tools สำหรับดึงข้อมูลจากตาราง Google Sheets 7 ไฟล์ และเชื่อมต่อกับ Google Drive API โดยตรง | รหัสโค้ด (Code) | โชว์ความสามารถในการเรียกใช้ Tool ในรูปแบบประหยัด Token เช่น ส่งเฉพาะรหัสโครงการเพื่ออ่านชีตย่อย แทนการดึงข้อมูลดิบทั้งหมด |
| **3. เครื่องมือ Antigravity** | **ใช้ Antigravity AI Coding Assistant ใน IDE ระหว่างการพัฒนา** เพื่อให้ช่วยออกแบบโค้ด จัดการหน่วยความจำ เขียนชุดทดสอบ และประยุกต์ใช้ในการตั้งระบบ Cron Job แจ้งเตือน | วิดีโอ (Video) | **[สำคัญมาก]** ในวิดีโอต้องแคปหน้าจอที่มีหน้าต่างแชตของ Antigravity IDE ปรากฏอยู่ คู่กับการรันโค้ด หรือโชว์ภาพประวัติการคุยพัฒนา และกล่าวในบทพูดว่ามี Antigravity เป็นผู้ช่วยพัฒนา |
| **4. ฟีเจอร์ด้านความปลอดภัย** | พัฒนา `app/security.py` เพื่อกรองข้อมูลอ่อนไหว (PII) เช่น ลบชื่อจริง/เบอร์โทรศัพท์/อีเมลส่วนตัว หรือรหัสผ่าน ก่อนส่งเข้า LLMภายนอก และเก็บ Google Credentials ไว้ใน `.env` | รหัสโค้ด หรือ วิดีโอ (Code or Video) | แสดงคำสั่งทดสอบ `test_security.py` เพื่อพิสูดระบบการล้างข้อมูล PII ก่อนยิง API |
| **5. ความสามารถในการปรับใช้งาน (Deployability)** | รันระบบด้วย Streamlit Web UI และจัดการ dependencies ทั้งหมดด้วย `pyproject.toml` ผ่าน Astral `uv` | วิดีโอ (Video) | โชว์หน้าจอตอนติดตั้งผ่าน `uv pip install -r requirements.txt` หรือ `uv run python main.py` และการแสดงผลลัพธ์ผ่านหน้าจอ Web Dashboard |
| **6. ทักษะของเอเจนต์ (เช่น Agents CLI)** | กำหนดพฤติกรรมคำสั่งของเอเจนต์อย่างมีระบบผ่านโมดูล Skills ภายใต้โฟลเดอร์ `.agents/skills/` | รหัสโค้ด หรือ วิดีโอ (Code or Video) | จัดทำไฟล์คู่มือ `README.md` อธิบายคำสั่งที่ CLI/Web UI สามารถรองรับทั้ง 5 รูปแบบ |

---

## 🏗️ Complete Project Directory Structure

```text
d:\_WORK\Project_2569\ProjectAIAgent/
├── .agents/
│   └── skills/                         # 💡 4 Modular Agent Skills (.agents/skills/)
│       ├── roadmap-fetching/
│       │   └── SKILL.md                # Skill 0: อ่านคัดกรองข้อมูลจากชีต "Project" และชีตรหัส "ST*"
│       ├── timeline-risk-assessment/
│       │   └── SKILL.md                # Skill 1: ตรวจจับเดดไลน์ คำนวณความคืบหน้าเฉลี่ย และประเมินความล่าช้า
│       ├── resource-optimization/
│       │   └── SKILL.md                # Skill 2: กรองพนักงานที่ไม่มีงาน Doing และจับคู่ผู้รับงานใหม่
│       └── weekly-report-summarizer/
│           └── SKILL.md                # Skill 3: รวบรวมงานย่อยรายสัปดาห์สร้างบทสรุปผู้บริหาร
├── app/
│   ├── __init__.py
│   ├── agent.py                        # ADK 2.0 Multi-Agent Orchestrator
│   ├── security.py                     # ระบบล้างข้อมูล PII (PII Scrubbing - ชื่อ, เบอร์โทร, อีเมล)
│   ├── session_manager.py              # SQLite Persistent Storage เก็บประวัติแชตและ Cache ข้อมูลชีตเพื่อเลี่ยง API Rate Limit
│   └── utils.py                        # ฟังก์ชันช่วยเหลือ (แปลงรูปแบบวันที่ไทย/สากล, จัดการโครงสร้างข้อมูลตาราง)
├── database/
│   ├── mock_roadmap.json               # ข้อมูลแผนงานจำลองของทั้ง 7 ทีม (สำหรับรันชุดทดสอบออฟไลน์)
│   └── sessions.db                     # SQLite Database เก็บเซสชัน
├── mcp_server.py                       # FastMCP Server เผยแพร่ Tools เชื่อม Google Sheets & Drive
├── main.py                             # Web Dashboard Portal (Streamlit App)
├── tests/                              # ชุดทดสอบอัตโนมัติ (Pytest Integration & Unit Tests)
│   ├── test_security.py
│   ├── test_mcp.py
│   └── test_agent_workflow.py
├── .env.example                        # ไฟล์จำลองตั้งค่าคีย์ API และ Google API Credentials
├── README.md                           # คู่มือโครงการฉบับสมบูรณ์สำหรับกรรมการตรวจประเมิน
└── pyproject.toml                      # การตั้งค่า dependencies ของโครงการด้วย uv
```

---

## 🛠️ Detailed Component Implementation Plan

### Phase 1: Modular Agent Skills (`.agents/skills/`)

#### 1. [NEW] [.agents/skills/roadmap-fetching/SKILL.md](file:///d:/_WORK/Project_2569/ProjectAIAgent/.agents/skills/roadmap-fetching/SKILL.md)
* **เป้าหมาย:** สกัดข้อมูลโครงสร้างแผนงานจากตารางระดับ Macro (`Project`) และระดับ Micro (`ST*`)
* **ข้อกำหนดการประมวลผล:**
  * อ่านเฉพาะชีตที่ชื่อเท่ากับ `"Project"` หรือชีตย่อยที่ขึ้นต้นด้วยตัวอักษร `"ST"` ตามด้วยตัวเลข เช่น `ST1`, `ST2` เท่านั้น (ข้ามชีตคำอธิบายหรือข้อมูลอื่น)
  * จัดกลุ่มหัวตาราง: ชีต `Project` ดึงข้อมูลคอลัมน์ B (รหัส), C (ระบบ), E (หัวหน้า), F (ทีมงาน), H-I (วันเริ่ม-เสร็จ), J (เดดไลน์), K (สถานะ), N (ความคืบหน้า), P (หมายเหตุ) ส่วนชีต `ST*` ดึงชื่องานย่อย, ผู้รับผิดชอบ, สถานะ (To Do / Doing / Done) และหมายเหตุรายชิ้นงาน

#### 2. [NEW] [.agents/skills/timeline-risk-assessment/SKILL.md](file:///d:/_WORK/Project_2569/ProjectAIAgent/.agents/skills/timeline-risk-assessment/SKILL.md)
* **เป้าหมาย:** วิเคราะห์สถานะความคืบหน้า (%) และโอกาสความล่าช้าของระบบ
* **ข้อกำหนดการประมวลผล:**
  * คำนวณวันส่งมอบเทียบกับความคืบหน้าปัจจุบัน หากความคืบหน้าต่ำกว่าเกณฑ์ในขณะใกล้เดดไลน์ ให้ประเมินระดับความเสี่ยงเป็น High/Medium/Low
  * ตัวอย่าง: เมื่อได้รับคำสั่งถามถึง *"ระบบบรรจุ"* ให้ค้นหาระบบนี้ในชีต `Project` ดึง % ความคืบหน้า (คอลัมน์ N) และวันส่งมอบ (คอลัมน์ J) ของ **ทีมพี่ไก่ (จิราภา)** มาวิเคราะห์ความเสี่ยงเสร็จไม่ทัน

#### 3. [NEW] [.agents/skills/resource-optimization/SKILL.md](file:///d:/_WORK/Project_2569/ProjectAIAgent/.agents/skills/resource-optimization/SKILL.md)
* **เป้าหมาย:** ตรวจสอบผู้ที่มีคิวงานว่าง (Gap Analysis) และจัดสรรทรัพยากรพนักงาน
* **ข้อกำหนดการประมวลผล:**
  * กรองรายชื่อพนักงานทั้งหมด 16 คนข้าม 7 ไฟล์ชีต คัดรายชื่อคนที่ **ไม่มีสถานะงานเป็น 'doing'** เลยในทุกๆ โครงการออกมานำเสนอ
  * เมื่อมีงานด่วนเข้ามา ให้ตรวจสอบคนที่เหมาะสมตามทักษะและความว่าง

#### 4. [NEW] [.agents/skills/weekly-report-summarizer/SKILL.md](file:///d:/_WORK/Project_2569/ProjectAIAgent/.agents/skills/weekly-report-summarizer/SKILL.md)
* **เป้าหมาย:** สร้างสรุปรายงานผลโครงการรายสัปดาห์
* **การทำงาน:** ดึงความเคลื่อนไหวจากทุกทีม สรุปจำนวนโครงการที่เสร็จสิ้น (Done) งานที่หยุดชะงัก (Paused) หรือ Backlog แยกรายทีม

---

### Phase 2: Knowledge Base & FastMCP Server (`mcp_server.py`)

#### 1. [NEW] [mcp_server.py](file:///d:/_WORK/Project_2569/ProjectAIAgent/mcp_server.py)
* สร้างเซิร์ฟเวอร์ MCP โดยใช้ `FastMCP` กำหนดขอบเขตความสามารถ:
  * `@mcp.tool() def fetch_project_summary(sheet_id: str) -> list[dict]`: สแกนชีต `Project` ของทีมนั้นๆ ดึงภาพรวมโครงการออกมา
  * `@mcp.tool() def fetch_st_detail(sheet_id: str, st_code: str) -> list[dict]`: อ่านข้อมูลรายละเอียดงานย่อยจากชีตรหัส `ST*` (เช่น ST1, ST2)
  * `@mcp.tool() def write_status_update(sheet_id: str, st_code: str, task_row: int, new_status: str) -> str`: อัปเดตสถานะงานย่อยกลับไปยังเซลล์ใน Google Sheets จริง

---

### Phase 3: Core Logic, Security & Sessions (`app/`)

#### 1. [NEW] [app/security.py](file:///d:/_WORK/Project_2569/ProjectAIAgent/app/security.py)
* ฟังก์ชัน `clean_pii_context(raw_data: list/dict) -> list/dict`:
  * คัดกรองและเซ็นเซอร์ข้อมูลอีเมลพนักงาน เบอร์โทรศัพท์ส่วนตัว และรหัสความปลอดภัยอื่นๆ ก่อนที่จะทำการป้อนเข้าสู่ LLM โมเดลภายนอก เพื่อไม่ให้ละเมิดนโยบายด้านความปลอดภัยทางข้อมูล

#### 2. [NEW] [app/session_manager.py](file:///d:/_WORK/Project_2569/ProjectAIAgent/app/session_manager.py)
* สร้างระบบบันทึกความทรงจำระยะสั้นและยาวในตาราง SQLite:
  * บันทึกคำถาม-คำตอบย้อนหลัง
  * มีระบบ Cache ข้อมูลชีตเพื่อลดอัตราความถี่การยิง API ป้องกันปัญหา Google API Quota Exceeded (จำกัดไม่ให้ยิง API บ่อยเกินไป)

#### 3. [NEW] [app/agent.py](file:///d:/_WORK/Project_2569/ProjectAIAgent/app/agent.py)
* ประสานงานระหว่างเอเจนต์ย่อยโดยสร้างโครงสร้าง Workflow:
  1. รับคำสั่งผู้ใช้ $\rightarrow$ 2. ตรวจสอบว่าต้องอ่านชีต Project หรือชีต ST $\rightarrow$ 3. เรียกใช้งานเครื่องมือ MCP เพื่อกวาดข้อมูล $\rightarrow$ 4. นำผลลัพธ์ผ่านความปลอดภัย (Security Check) $\rightarrow$ 5. ส่งผลวิเคราะห์คืนผู้ใช้

---

### Phase 4: Web Application Portal & Testing (`main.py` & `tests/`)

#### 1. [NEW] [main.py](file:///d:/_WORK/Project_2569/ProjectAIAgent/main.py)
* พัฒนาหน้าจอ Dashboard ด้วย Streamlit:
  * แสดงแท็บข้อมูลของทั้ง 7 ทีม
  * ช่องสนทนากับ AI Agent ที่รองรับการถามคำถามภาษาไทยทั้ง 5 รูปแบบที่กำหนด
  * หน้าตารางเปรียบเทียบ Workload ของสมาชิกทีมทั้งหมด 16 คน พร้อมระบุคนที่คิวว่าง (ไม่มีงาน Doing)

#### 2. [NEW] [tests/](file:///d:/_WORK/Project_2569/ProjectAIAgent/tests/)
* ชุดทดสอบสำหรับรับประกันการทำงานผ่านคำสั่ง `pytest`:
  * `test_security.py`: ทดสอบการกรองข้อมูล PII
  * `test_mcp.py`: ทดสอบการเรียกฟังก์ชันดึงชีต Project และชีต ST*
  * `test_agent_workflow.py`: ทดสอบการถามคำถาม 5 รูปแบบเทียบกับข้อมูล Mock ในไฟล์ `mock_roadmap.json`

---

## 🧪 Detailed Verification & Validation Plan

### Automated Testing Suite (`uv run pytest`)
1. **Unit Test - ST Worksheet Pattern Matching:** ส่งชื่อชีตหลากหลายรูปแบบ ทดสอบความถูกต้องในการยอมรับเฉพาะชื่อที่ขึ้นต้นด้วย `ST` ตามด้วยตัวเลขเท่านั้น
2. **Integration Test - Cross-file Idle Search:** ทดสอบสั่งค้นหาคนว่างงานจำลองในระบบ คีย์คำสั่ง *"มีใครบ้างที่ไม่มีสถานะงานที่เป็น doing"* เช็กว่าสามารถหาพนักงานที่ว่างใน 7 ชีตได้ถูกต้องครบถ้วน
3. **Security Check - Credential Safety:** ยืนยันว่าเมื่อสั่งรัน คำสั่งไม่มีการเรียกค่า API Key ที่ Hardcode ไว้ และมีการใช้ระบบ Fallback ไปหาโมเดลสำรองเมื่อ API จำกัด

### Manual Verification & Demo Flow (สำหรับวิดีโอ 5 นาที)
1. **แนะนำ Pain Point:** แสดงภาพว่า IT Manager ต้องจัดการ 7 ทีม 16 คน และ 30+ ระบบย่อยในเบราว์เซอร์
2. **โชว์ Antigravity:** แสดงประวัติการถามตอบและโค้ดของโปรเจกต์ที่พัฒนาร่วมกับ **Antigravity AI Assistant** ในหน้าต่าง IDE
3. **ทดสอบคำถามรายบุคคล:** พิมพ์ค้นหาประวัติงานย่อยของ พีท/เมล์ บนแอป Streamlit และแสดงผลลิสต์งานทันที
4. **ทดสอบระบบความเสี่ยง (ระบบบรรจุ):** พิมพ์ถามสถานะและเดดไลน์ระบบบรรจุของทีมพี่ไก่ ตรวจสอบความถูกต้องของคำตอบ
5. **ทดสอบคนว่างงาน (No Doing Task):** พิมพ์หาพนักงานที่ว่างอยู่เพื่อกระจายงานใหม่
6. **ทดสอบ Real-time Update:** แกล้งเปลี่ยนสถานะงานย่อยจาก "Doing" เป็น "Done" บนหน้า Google Sheet ในเบราว์เซอร์ แล้วกลับมาถาม AI ในแอปเพื่อโชว์ความสามารถแบบสดใหม่เสมอ
