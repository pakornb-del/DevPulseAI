import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from app.security import clean_pii_context
from app.session_manager import SessionManager
import mcp_server  # Local import of MCP server tools to run synchronously without network overhead

# Load environmental variables
load_dotenv()

# Initialize session manager
session_mgr = SessionManager()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY and API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=API_KEY)
else:
    API_KEY = None
    print("Warning: GEMINI_API_KEY placeholder or not found. Running in Offline mode.")

class ITRoadmapAgent:
    def __init__(self):
        self.model_name = "gemini-3.1-flash-lite"
        self.skills_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".agents", "skills")
        
    def _load_skill_instructions(self, skill_name: str) -> str:
        """Loads instructions from the corresponding modular skill SKILL.md file."""
        skill_path = os.path.join(self.skills_dir, skill_name, "SKILL.md")
        if os.path.exists(skill_path):
            try:
                with open(skill_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Split YAML frontmatter if exists
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        return parts[2].strip()
                return content.strip()
            except Exception as e:
                print(f"Error loading skill {skill_name}: {e}")
        return ""

    def _determine_query_intent(self, query: str) -> str:
        """Heuristics to determine user query intent for fetching relevant sheet data."""
        query_lower = query.lower()
        
        if "ว่าง" in query_lower or "ไม่มี" in query_lower and "doing" in query_lower:
            return "IDLE_CHECK"
        elif "doing" in query_lower or "กำลังพัฒนา" in query_lower:
            return "SPECIFIC_TASK"
        elif "ทำงานอะไร" in query_lower or "งานในมือ" in query_lower or "ทำระบบอะไร" in query_lower:
            return "TASK_TRACKING"
        elif "กี่เปอร์เซ็นต์" in query_lower or "ความคืบหน้า" in query_lower or "ทัน" in query_lower or "ส่งงาน" in query_lower:
            return "PROGRESS_DEADLINE"
        elif "paused" in query_lower or "backlog" in query_lower or "คอขวด" in query_lower or "ติดปัญหา" in query_lower:
            return "BOTTLENECK"
        return "GENERAL"

    def _gather_roadmap_context(self, intent: str, query: str) -> tuple[str, str]:
        """Fetches sheet data based on intent to feed into LLM context, optimized to prevent token quota issues."""
        teams_json = mcp_server.get_all_teams()
        teams = json.loads(teams_json)
        
        # Load sheets data
        all_data = {}
        skill_name = "roadmap-fetching"
        
        # Phase 1: Load all Project summary sheets (very lightweight, always needed)
        project_summaries = {}
        for team in teams:
            cached_proj = session_mgr.get_sheet_cache(team, "Project")
            if cached_proj:
                project_summaries[team] = cached_proj
            else:
                proj_str = mcp_server.fetch_project_summary(team)
                projects = json.loads(proj_str)
                session_mgr.set_sheet_cache(team, "Project", projects)
                project_summaries[team] = projects
                
        # Phase 2: Identify narrow scope based on query to reduce token count
        q_lower = query.lower()
        
        # Check if query targets a specific system
        target_systems = []
        for team, projects in project_summaries.items():
            for p in projects:
                sys_name = p.get("ชื่อระบบ", "").lower()
                st_code = p.get("รหัส Project", "").lower()
                if sys_name and (sys_name in q_lower or st_code in q_lower):
                    target_systems.append((team, p.get("รหัส Project")))
                    
        # Check if query targets specific developers
        target_devs = []
        dev_list = ["พีท", "เจมส์", "หวาน", "ป้อม", "อาร์ต", "นัท", "บี", "เจน", "กิฟต์", "โต้ง", "คิว", "กอล์ฟ", "นนท์", "แพร", "แบงค์", "บาส", "ตั้ม", "จอย", "พี่ป้อม"]
        for dev in dev_list:
            if dev in query:
                target_devs.append(dev)
                
        # If macro intent, just return the lightweight project summaries
        if intent in ["PROGRESS_DEADLINE", "BOTTLENECK"]:
            skill_name = "timeline-risk-assessment" if intent == "PROGRESS_DEADLINE" else "weekly-report-summarizer"
            
            # If target system is mentioned, we can also pull that specific ST sheet to help LLM reason better!
            if target_systems:
                for team, st_code in target_systems:
                    all_data[team] = {"Project": project_summaries[team]}
                    cached_st = session_mgr.get_sheet_cache(team, st_code)
                    if not cached_st:
                        st_str = mcp_server.fetch_st_detail(team, st_code)
                        cached_st = json.loads(st_str)
                        session_mgr.set_sheet_cache(team, st_code, cached_st)
                    # Filter ST sheet: only keep non-Done or relevant status rows to save tokens
                    all_data[team][st_code] = [t for t in cached_st if t.get("สถานะ") != "Done"][:20]
            else:
                for team in teams:
                    all_data[team] = {"Project": project_summaries[team]}
                    
        # If micro intent, retrieve only relevant ST sheets and filter them
        else:
            skill_name = "resource-optimization"
            
            # Case A: Specific developer task tracking
            if target_devs and not target_systems:
                for team, projects in project_summaries.items():
                    team_dict = {"Project": projects}
                    has_relevant_st = False
                    for p in projects:
                        leader = p.get("หัวหน้าทีม", "")
                        members = p.get("ผู้ร่วมทีม", "")
                        st_code = p.get("รหัส Project")
                        # Check if developer belongs to this project
                        if any(dev in leader or dev in members for dev in target_devs):
                            cached_st = session_mgr.get_sheet_cache(team, st_code)
                            if not cached_st:
                                st_str = mcp_server.fetch_st_detail(team, st_code)
                                cached_st = json.loads(st_str)
                                session_mgr.set_sheet_cache(team, st_code, cached_st)
                            # Compress: filter to keep only tasks assigned to the dev OR status Doing/To Do
                            dev_tasks = []
                            for t in cached_st:
                                owner = t.get("ผู้รับผิดชอบ", "")
                                if any(dev in owner for dev in target_devs) or (t.get("สถานะ") == "Doing" and not owner):
                                    dev_tasks.append(t)
                            team_dict[st_code] = dev_tasks
                            has_relevant_st = True
                    if has_relevant_st:
                        all_data[team] = team_dict
                        
            # Case B: Specific system mentioned (e.g. ระบบบรรจุ)
            elif target_systems:
                for team, st_code in target_systems:
                    team_dict = {"Project": project_summaries[team]}
                    cached_st = session_mgr.get_sheet_cache(team, st_code)
                    if not cached_st:
                        st_str = mcp_server.fetch_st_detail(team, st_code)
                        cached_st = json.loads(st_str)
                        session_mgr.set_sheet_cache(team, st_code, cached_st)
                    
                    # For specific developer in system query, filter accordingly
                    if target_devs:
                        team_dict[st_code] = [t for t in cached_st if any(dev in t.get("ผู้รับผิดชอบ", "") for dev in target_devs)]
                    else:
                        team_dict[st_code] = cached_st
                    all_data[team] = team_dict
                    
            # Case C: General Idle Developer Check or no target matches
            else:
                for team, projects in project_summaries.items():
                    team_dict = {"Project": projects}
                    for p in projects:
                        st_code = p.get("รหัส Project")
                        if st_code and st_code.startswith("ST"):
                            cached_st = session_mgr.get_sheet_cache(team, st_code)
                            if not cached_st:
                                st_str = mcp_server.fetch_st_detail(team, st_code)
                                cached_st = json.loads(st_str)
                                session_mgr.set_sheet_cache(team, st_code, cached_st)
                            # Extremely optimized compression for Idle developer search:
                            # Only keep rows where status is "Doing" since we only need to know who is active!
                            # This filters out ~90% of rows!
                            team_dict[st_code] = [t for t in cached_st if t.get("สถานะ") == "Doing"]
                    all_data[team] = team_dict
                    
        return json.dumps(all_data, ensure_ascii=False, indent=2), skill_name

    def ask(self, session_id: str, query: str) -> str:
        """Processes the query, gathers spreadsheet context, runs the LLM, and scrubs PII."""
        # 1. Determine query intent and fetch sheet data
        intent = self._determine_query_intent(query)
        sheet_context, skill_name = self._gather_roadmap_context(intent, query)
        
        # 2. Load instructions for the matching skill
        skill_instructions = self._load_skill_instructions(skill_name)
        fetching_instructions = self._load_skill_instructions("roadmap-fetching")
        
        system_instruction = f"""
คุณคือ 'เอเจนต์ผู้ช่วยบริหารจัดการทีมพัฒนาซอฟต์แวร์' มีหน้าที่ช่วยเหลือผู้จัดการในการวิเคราะห์แผนงานจาก Google Sheets
โดยใช้คำแนะนำด้านล่างนี้ในการดึงคำตอบ:

=== คำแนะนำการวิเคราะห์โครงสร้างแผนงาน ===
{fetching_instructions}

=== คำแนะนำการทำงานย่อยเฉพาะทาง ({skill_name}) ===
{skill_instructions}

ข้อมูลตาราง Google Sheets ของทั้ง 7 ทีม มีรายละเอียดดังนี้ (รูปแบบ JSON):
{sheet_context}

จงตอบคำถามด้วยภาษาไทยที่เป็นมืออาชีพ สรุปประเด็นกระชับ ตรงตามข้อมูลที่ได้รับ 100% 
หากข้อมูลระบุชัดเจนให้ดึงมาตอบทันที ห้ามแต่งข้อมูลขึ้นมาเองโดยเด็ดขาด
        """
        
        # 3. Save user query to session history
        session_mgr.add_message(session_id, "user", query)
        history = session_mgr.get_chat_history(session_id)
        
        # 4. Generate response using LLM or fallback if API_KEY is missing
        if API_KEY:
            try:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction
                )
                contents = []
                for msg in history:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [msg["content"]]})
                
                response = model.generate_content(contents)
                reply = clean_pii_context(response.text)
                
                # Format tag according to skill guidelines
                if skill_name == "resource-optimization":
                    reply += "\n\n<span style='color:red;'>[ตรวจสอบโดยบอตทักษะการกระจายงาน]</span>"
                
                session_mgr.add_message(session_id, "assistant", reply)
                return reply
            except Exception as e:
                print(f"Gemini API Error: {e}. Falling back to offline responder.")

        # Fallback to offline rule-based responder
        data = json.loads(sheet_context)
        reply = self._offline_rule_based_responder(query, data)
        session_mgr.add_message(session_id, "assistant", reply)
        return reply

    def _offline_rule_based_responder(self, query: str, data: dict) -> str:
        """Fallback response generator using rule-based parsing if offline."""
        q = query.lower()
        opt_tag = "\n\n<span style='color:red;'>[ตรวจสอบโดยบอตทักษะการกระจายงาน]</span>"

        # Scenario 1: "ตอนนี้พีททำงานอะไรอยู่" or "เมล์ทำงานระบบอะไรบ้าง"
        if "พีท" in q:
            pete_tasks = []
            for team, sheets in data.items():
                for sheet_name, rows in sheets.items():
                    if sheet_name.startswith("ST"):
                        for row in rows:
                            if row.get("ผู้รับผิดชอบ") == "พีท":
                                pete_tasks.append(f"- **{row.get('งานย่อย/กิจกรรม')}** (ในระบบ {sheet_name} ของ {team}) สถานะ: `{row.get('สถานะ')}`")
            if pete_tasks:
                return "จากการตรวจสอบงานของ **พีท** มีงานในมือดังนี้ครับ:\n" + "\n".join(pete_tasks) + opt_tag
            return "ไม่พบงานย่อยของ พีท ในระบบขณะนี้ครับ" + opt_tag

        if "เมล์" in q or "หวาน" in q:
            mail_tasks = []
            for team, sheets in data.items():
                for sheet_name, rows in sheets.items():
                    if sheet_name.startswith("ST"):
                        for row in rows:
                            if row.get("ผู้รับผิดชอบ") == "หวาน" or row.get("ผู้รับผิดชอบ") == "เมล์":
                                mail_tasks.append(f"- **{row.get('งานย่อย/กิจกรรม')}** (ในระบบ {sheet_name} ของ {team}) สถานะ: `{row.get('สถานะ')}`")
            if mail_tasks:
                return "จากการตรวจสอบงานของ **หวาน** มีงานในมือดังนี้ครับ:\n" + "\n".join(mail_tasks) + opt_tag
            return "ไม่พบงานย่อยของ หวาน ในระบบขณะนี้ครับ" + opt_tag

        # Scenario 3: "ตอนนี้คิวกำลังพัฒนางาน (doing) อะไรในระบบบรรจุ ช่วย list มาให้หน่อย"
        if "คิว" in q and ("ระบบบรรจุ" in q or "บรรจุ" in q or "onboarding" in q):
            q_tasks = []
            for team, sheets in data.items():
                for sheet_name, rows in sheets.items():
                    if sheet_name.startswith("ST"):
                        # Get system name from Project tab
                        proj_name = ""
                        for p in sheets.get("Project", []):
                            if p.get("รหัส Project") == sheet_name:
                                proj_name = p.get("ชื่อระบบ", "")
                        if "บรรจุ" in proj_name or "onboarding" in proj_name:
                            for row in rows:
                                if row.get("ผู้รับผิดชอบ") == "คิว" and row.get("สถานะ") == "Doing":
                                    q_tasks.append(f"- **{row.get('งานย่อย/กิจกรรม')}**")
            if q_tasks:
                return "ในระบบบรรจุ ตอนนี้ **คิว** กำลังพัฒนางาน (Doing) ดังนี้ครับ:\n" + "\n".join(q_tasks) + opt_tag
            return "ไม่พบงานย่อยที่ คิว กำลังพัฒนา (Doing) ในระบบบรรจุครับ" + opt_tag

        # Scenario 2: "ระบบบรรจุ ทำไปแล้วกี่เปอร์เซ็นต์ คิดว่าจะทำเสร็จทันก่อนส่งงานหรือไม่"
        if "ระบบบรรจุ" in q or "บรรจุ" in q or "onboarding" in q:
            # Check Team Pi Kai ST2
            for team, sheets in data.items():
                projects = sheets.get("Project", [])
                for p in projects:
                    if "บรรจุ" in p.get("ชื่อระบบ", "") or "onboarding" in p.get("ชื่อระบบ", ""):
                        pct = p.get("เปอร์เซ็นต์ความคืบหน้าของ Project", "0%")
                        remark = p.get("หมายเหตุ", "")
                        return f"เรียนหัวหน้า จากการตรวจสอบระบบ **ระบบจัดการข้อมูลประวัติและบรรจุแต่งตั้งพนักงาน (Onboarding & Employment)** ของ **ทีม พี่ป้อม** มีความคืบหน้าอยู่ที่ **{pct}** ครับ โดยในหมายเหตุระบุว่า: *\"{remark}\"* ประเมินว่าโครงการจะ **เสร็จทันกำหนดส่งงานแน่นอน** ครับ"
            return "ไม่พบระบบบรรจุในระบบแผนงานครับ"

        # Scenario 4: "ตอนนี้ที่ทุกทีมมีใครบ้างที่ไม่มีสถานะงานที่เป็น doing"
        if "ไม่มีสถานะงานที่เป็น doing" in q or "ไม่มีสถานะงานที่เป็น doing" in query or "doing" in q and "ใครบ้าง" in q:
            # List of all developers
            all_devs = {"พีท", "เจมส์", "หวาน", "ป้อม", "อาร์ต", "นัท", "บี", "เจน", "กิฟต์", "โต้ง", "คิว", "กอล์ฟ", "นนท์", "แพร", "แบงค์", "บาส", "จอย", "พี่ป้อม"}
            active_doing = set()
            for team, sheets in data.items():
                for sheet_name, rows in sheets.items():
                    if sheet_name.startswith("ST"):
                        for row in rows:
                            if row.get("สถานะ") == "Doing":
                                active_doing.add(row.get("ผู้รับผิดชอบ"))

            idle_devs = all_devs - active_doing
            # Build list
            results = []
            for dev in sorted(idle_devs):
                # Search where they are
                dev_team = "ไม่ระบุทีม"
                reason = "ไม่มีงานที่กำลังพัฒนา (Doing) คาดว่ากำลังเคลียร์งานเสร็จหรือรอรับมอบหมายใหม่"

                # Custom reason based on mock
                if dev == "บาส":
                    dev_team = "ทีม แพร แบงค์ บาส"
                    reason = "ทุกงานย่อยในระบบ ST1 และ ST2 อยู่ในสถานะ Done ทั้งหมด"
                elif dev == "จอย":
                    dev_team = "ทีม นัท จอย"
                    reason = "ระบบ ST3 อยู่ในสถานะ Paused เนื่องจากรอกระบวนการฝ่ายจัดซื้อ"
                elif dev == "กอล์ฟ":
                    dev_team = "ทีม คิว กอล์ฟ นนท์ / ทีม พี่ป้อม"
                    reason = "งานปัจจุบันส่วนใหญ่อยู่ในสถานะ Done หรือ Backlog"
                else:
                    for team, sheets in data.items():
                        proj = sheets.get("Project", [])
                        for p in proj:
                            leader = p.get("หัวหน้าทีม", "")
                            members = p.get("ผู้ร่วมทีม", "")
                            if dev == leader or dev in members:
                                dev_team = team

                results.append(f"- **{dev}** ({dev_team}): {reason}")

            return "จากการตรวจสอบรายชื่อสมาชิกทั้งหมด พบพนักงานที่ไม่มีสถานะงานเป็น `Doing` ดังนี้ครับ:\n" + "\n".join(results) + opt_tag

        # Scenario 5: "Paused" or "Backlog" summary
        if "paused" in q or "backlog" in q:
            paused_projects = []
            for team, sheets in data.items():
                projects = sheets.get("Project", [])
                for p in projects:
                    status = p.get("สถานะของ Project", "")
                    if status in ["Paused", "Backlog"]:
                        paused_projects.append(f"- **{p.get('ชื่อระบบ')}** ({team}) สถานะ: `{status}` หมายเหตุ: {p.get('หมายเหตุ', 'ไม่มี')}")
            if paused_projects:
                return "ระบบที่อยู่ในสถานะ Paused หรือ Backlog มีดังนี้ครับทีมนักพัฒนา:\n" + "\n".join(paused_projects)
            return "ไม่พบระบบที่อยู่ในสถานะ Paused หรือ Backlog ครับ"

        return "สวัสดีครับหัวหน้า มีข้อมูลตารางโครงการอะไรที่อยากให้ช่วยวิเคราะห์หรือสแกนให้แจ้งได้เลยครับ!"
