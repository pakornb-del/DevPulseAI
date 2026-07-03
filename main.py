import streamlit as st
import os
import uuid
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from app.agent import ITRoadmapAgent
from app.session_manager import SessionManager

# Set page config with dark/premium layout
st.set_page_config(
    page_title="DevPulse AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using CSS injection
st.markdown("""
<style>
    /* Main body background & typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sleek gradient headers */
    .gradient-text {
        background: linear-gradient(135deg, #FF8A00 0%, #E52E71 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 0.2rem;
    }
    .sub-text {
        color: #8892B0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* LINE Chat App layout styles */
    .chat-bubble-container {
        display: flex;
        width: 100%;
        margin-bottom: 12px;
    }
    .user-container {
        justify-content: flex-end;
    }
    .assistant-container {
        justify-content: flex-start;
    }
    .chat-bubble-new {
        padding: 10px 14px;
        border-radius: 16px;
        max-width: 75%;
        font-size: 0.95rem;
        line-height: 1.4;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
        word-wrap: break-word;
    }
    .user-bubble-new {
        background-color: #06C755; /* LINE Green */
        color: #ffffff;
        border-top-right-radius: 4px;
    }
    .assistant-bubble-new {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid rgba(255, 138, 0, 0.4);
        border-top-left-radius: 4px;
    }
    
    /* Interactive Cards */
    .info-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 138, 0, 0.3);
    }
    
    /* Table Styling */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session Manager and Agent
session_mgr = SessionManager()
agent = ITRoadmapAgent()

def markdown_to_html(text: str) -> str:
    import re
    # 1. Escape HTML
    html = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # 2. Format code blocks
    def code_block_sub(match):
        code = match.group(1)
        return f'<pre style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; overflow-x: auto; font-family: monospace; white-space: pre-wrap; word-break: break-all;"><code>{code}</code></pre>'
    html = re.sub(r'```(?:python|json|text|bash)?\n(.*?)\n```', code_block_sub, html, flags=re.DOTALL)
    
    # 3. Format inline code
    html = re.sub(r'`(.*?)`', r'<code style="background: rgba(0,0,0,0.25); padding: 2px 4px; border-radius: 4px; font-family: monospace;">\1</code>', html)
    
    # 4. Format bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # 5. Format headers
    html = re.sub(r'^### (.*?)$', r'<h5 style="margin: 8px 0 4px 0; font-weight: bold;">\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h4 style="margin: 10px 0 6px 0; font-weight: bold;">\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h3 style="margin: 12px 0 8px 0; font-weight: bold;">\1</h3>', html, flags=re.MULTILINE)
    
    # 6. Format lists
    lines = html.split('\n')
    new_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('*') or stripped.startswith('-'):
            item_text = stripped[1:].strip()
            if not in_list:
                new_lines.append('<ul style="margin: 4px 0; padding-left: 20px;">')
                in_list = True
            new_lines.append(f'<li style="margin-bottom: 2px;">{item_text}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)
    if in_list:
        new_lines.append('</ul>')
    
    html = '\n'.join(new_lines)
    html = html.replace('\n', '<br>')
    html = re.sub(r'(<br>\s*){2,}', '<br><br>', html)
    html = html.replace('</ul><br>', '</ul>')
    html = html.replace('</pre><br>', '</pre>')
    html = html.replace('</h5><br>', '</h5>')
    html = html.replace('</h4><br>', '</h4>')
    # Force [ตรวจสอบโดยบอตทักษะการกระจายงาน] to be red and bold as requested by resource-optimization skill
    html = re.sub(
        r'(?:\*\*|<strong>|&lt;strong&gt;)?\[ตรวจสอบโดยบอตทักษะการกระจายงาน\](?:\*\*|</strong>|&lt;/strong&gt;)?',
        r'<span style="color: #ff4b4b; font-weight: bold;">[ตรวจสอบโดยบอตทักษะการกระจายงาน]</span>',
        html
    )
    
    return html

def format_timestamp(ts_str: str) -> str:
    try:
        # Handle datetime object or ISO string
        if isinstance(ts_str, str):
            dt = datetime.fromisoformat(ts_str)
        else:
            dt = ts_str
        time_str = dt.strftime("%H:%M")
        thai_months = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
        month_name = thai_months[dt.month - 1]
        thai_year = (dt.year + 543) % 100
        return f"{dt.day:02d} {month_name} {thai_year:02d} {time_str} น."
    except Exception:
        return ""

# Auto-refresh cache if it contains mock data but we have real Google Sheets configured in env
has_real_urls = any(os.getenv(k) and "docs.google.com" in os.getenv(k) for k in ["GOOGLE_SHEET_PDM_URL", "GOOGLE_SHEET_KAI_URL"])
if has_real_urls:
    cached_pdm = session_mgr.get_sheet_cache("ทีม พีท เจมส์ หวาน", "Project")
    if cached_pdm and len(cached_pdm) > 0:
        first_project_name = cached_pdm[0].get("ชื่อระบบ", "")
        if "On-Duty" in first_project_name or not first_project_name:
            session_mgr.clear_all_caches()
            st.rerun()

# Helper for Session Management
if "current_session_id" not in st.session_state:
    sessions = session_mgr.get_all_sessions()
    if sessions:
        st.session_state["current_session_id"] = sessions[0]["session_id"]
    else:
        # Create a default session
        default_id = str(uuid.uuid4())
        session_mgr.create_session(default_id, "Session 1: Initial Dashboard")
        st.session_state["current_session_id"] = default_id

# Sidebar Controls
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/artificial-intelligence.png", width=70)
    st.markdown("### 🛠️ Configuration & Sessions")
    
    # Refresh Cache Button
    if st.button("🔄 Clear & Refresh Sheets Cache", use_container_width=True):
        session_mgr.clear_all_caches()
        st.toast("Sheets cache database cleared successfully!", icon="💥")
        st.rerun()
        
    # Active Session Selector
    sessions = session_mgr.get_all_sessions()
    session_titles = {s["session_id"]: s["title"] for s in sessions}
    
    current_session = st.selectbox(
        "Select Conversation Session",
        options=list(session_titles.keys()),
        format_func=lambda x: session_titles[x],
        key="session_select"
    )
    if current_session:
        st.session_state["current_session_id"] = current_session
        
    # New Session Creator
    new_title = st.text_input("New Session Name", placeholder="e.g. Weekly Review")
    if st.button("➕ Create New Session", use_container_width=True) and new_title.strip():
        new_id = str(uuid.uuid4())
        session_mgr.create_session(new_id, new_title.strip())
        st.session_state["current_session_id"] = new_id
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 👥 IT Team Directory")
    st.markdown("""
    **16 Developers across 7 Teams:**
    * **ทีม พีท เจมส์ หวาน:** พีท, เจมส์, หวาน
    * **ทีม ป้อม อาร์ต นัท บี:** ป้อม, อาร์ต, นัท, บี
    * **ทีม เจน กิฟต์ โต้ง:** เจน, กิฟต์, โต้ง
    * **ทีม คิว กอล์ฟ นนท์:** คิว, กอล์ฟ, นนท์
    * **ทีม แพร แบงค์ บาส:** แพร, แบงค์, บาส
    * **ทีม นัท จอย:** นัท, จอย
    * **ทีม พี่ป้อม:** พี่ป้อม
    """)

# Main Content Layout
col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.markdown('<div class="gradient-text">DevPulse AI (เดฟพัลส์ เอไอ)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">เอเจนต์อัจฉริยะสำหรับตรวจสอบแผนงานและจัดสรรทรัพยากรผู้พัฒนาข้ามทีม<br><small style="font-size: 0.85rem; opacity: 0.85;">Multi-Team Roadmap Auditing and Resource Optimization Agent</small></div>', unsafe_allow_html=True)
    # Tab selector for GSheet summaries
    st.markdown("### 📋 Google Sheets Project Roadmap Summaries")
    
    # Try fetching team summary data
    teams = ["ทีม พีท เจมส์ หวาน", "ทีม ป้อม อาร์ต นัท บี", "ทีม เจน กิฟต์ โต้ง", "ทีม คิว กอล์ฟ นนท์", "ทีม แพร แบงค์ บาส", "ทีม นัท จอย", "ทีม พี่ป้อม"]
    tabs = st.tabs(teams)
    
    for idx, team in enumerate(teams):
        with tabs[idx]:
            # Load project overview list for the team
            cached = session_mgr.get_sheet_cache(team, "Project")
            if not cached:
                import mcp_server
                summary_str = mcp_server.fetch_project_summary(team)
                summary = json.loads(summary_str)
                session_mgr.set_sheet_cache(team, "Project", summary)
            else:
                summary = cached
                
            if summary:
                df = pd.DataFrame(summary)
                # Keep specific columns for display
                display_cols = ["รหัส Project", "ชื่อระบบ", "หัวหน้าทีม", "ผู้ร่วมทีม", "กำหนดส่งงาน", "สถานะของ Project", "เปอร์เซ็นต์ความคืบหน้าของ Project", "หมายเหตุ"]
                available_cols = [c for c in display_cols if c in df.columns]
                st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
            else:
                st.info("No project data found for this team.")
                
    st.markdown("---")
    with st.expander("⚙️ System Settings & API Configuration (สำหรับตั้งค่าระบบและย้ายโปรเจกต์)", expanded=False):
        st.markdown("#### 🔑 1. API Keys & Service Account Credentials")
        
        config_gemini_key = st.text_input("Gemini API Key:", value=os.getenv("GEMINI_API_KEY", ""), type="password")
        config_service_account_file = st.text_input("Google Service Account Key File Path:", value=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "credentials.json"))
        
        # Service Account JSON Text Area
        current_json_val = ""
        creds_path = os.path.join(os.path.dirname(__file__), config_service_account_file)
        if os.path.exists(creds_path):
            try:
                with open(creds_path, "r", encoding="utf-8") as f:
                    current_json_val = f.read()
            except Exception:
                pass
                
        config_service_account_json = st.text_area("Paste credentials.json Content (วางคีย์บริการบัญชีผู้ใช้):", value=current_json_val, height=150, help="นำเนื้อหาทั้งหมดในไฟล์ credentials.json ของ Service Account มาวางที่นี่เพื่อเชื่อม Google Drive")
        
        st.markdown("#### 📊 2. Google Sheets URLs Setup (ลิงก์ Google Sheets ทั้ง 7 ทีม)")
        
        # Render a form to group saves nicely
        url_inputs = {}
        team_env_vars = {
            "ทีม พีท เจมส์ หวาน": "GOOGLE_SHEET_PDM_URL",
            "ทีม ป้อม อาร์ต นัท บี": "GOOGLE_SHEET_KAI_URL",
            "ทีม เจน กิฟต์ โต้ง": "GOOGLE_SHEET_SU_URL",
            "ทีม คิว กอล์ฟ นนท์": "GOOGLE_SHEET_Q_URL",
            "ทีม แพร แบงค์ บาส": "GOOGLE_SHEET_FARBOOKMARK_URL",
            "ทีม นัท จอย": "GOOGLE_SHEET_OEITUK_URL",
            "ทีม พี่ป้อม": "GOOGLE_SHEET_JIRAPAH_URL"
        }
        
        for team_label, env_var in team_env_vars.items():
            url_inputs[env_var] = st.text_input(f"URL สำหรับ {team_label}:", value=os.getenv(env_var, ""))
            
        if st.button("💾 Save Settings & Refresh Cache", use_container_width=True):
            # Save to .env
            env_path = os.path.join(os.path.dirname(__file__), ".env")
            lines = []
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            
            new_config = {
                "GEMINI_API_KEY": config_gemini_key.strip(),
                "GOOGLE_SERVICE_ACCOUNT_FILE": config_service_account_file.strip(),
                "ENV": "development"
            }
            for env_var, url_val in url_inputs.items():
                new_config[env_var] = url_val.strip()
                
            updated_keys = set()
            new_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and "=" in stripped:
                    key, _ = stripped.split("=", 1)
                    key = key.strip()
                    if key in new_config:
                        new_lines.append(f"{key}={new_config[key]}\n")
                        updated_keys.add(key)
                        continue
                new_lines.append(line)
                
            for key, val in new_config.items():
                if key not in updated_keys:
                    new_lines.append(f"{key}={val}\n")
                    
            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
                
            # Save credentials.json if modified
            if config_service_account_json.strip():
                try:
                    json_data = json.loads(config_service_account_json)
                    with open(creds_path, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=2)
                except Exception as e:
                    st.error(f"Error parsing Service Account JSON: {e}")
                    
            # Clear Cache & Toast Success
            session_mgr.clear_all_caches()
            st.toast("System settings saved and database cache refreshed successfully! 🎉", icon="✅")
            st.rerun()

with col2:
    # Row with Chat Assistant header and a Clear Chat button
    col_header, col_clear = st.columns([0.65, 0.35])
    with col_header:
        st.markdown("### 💬 Chat Assistant")
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_chat_history_btn"):
            session_mgr.clear_session_chat(st.session_state["current_session_id"])
            st.toast("Chat history cleared!", icon="🧹")
            st.rerun()
            
    # Quick Commands dropdown (Selectbox instead of buttons) to save vertical space
    st.markdown("#### ⚡ Quick Actions (ยิงคำถามด่วน)")
    
    quick_queries = [
        ("👤 งานของพีท", "ตอนนี้พีททำงานอะไรอยู่"),
        ("📦 ระบบบรรจุ (ทีมพี่ไก่)", "ระบบบรรจุ ทำไปแล้วกี่เปอร์เซ็นต์ คิดว่าจะทำเสร็จทันก่อนส่งงานหรือไม่"),
        ("⚡ งาน Doing ของคิว", "ตอนนี้คิวกำลังพัฒนางาน (doing) อะไรในระบบบรรจุ ช่วย list มาให้หน่อย"),
        ("🆓 หาพนักงานว่าง (No Doing)", "ตอนนี้ที่ทุกทีมมีใครบ้างที่ไม่มีสถานะงานที่เป็น doing"),
        ("⚠️ งานสะดุด (Paused/Backlog)", "มีระบบไหนของทีมไหนบ้างที่มีสถานะเป็น Paused หรือ Backlog และมีหมายเหตุแจ้งว่าอะไร?")
    ]
    
    def on_quick_action_change():
        selected = st.session_state["quick_action_select_val"]
        if selected != "--- คลิกเลือกเพื่อยิงคำถามด่วน ---":
            label, query_text = selected.split(" -> ", 1)
            st.session_state["chat_input_val"] = query_text
            st.session_state["quick_action_select_val"] = "--- คลิกเลือกเพื่อยิงคำถามด่วน ---"

    st.selectbox(
        "เลือกหัวข้อคำถามเพื่อยิงทดสอบทันที:",
        options=["--- คลิกเลือกเพื่อยิงคำถามด่วน ---"] + [f"{q[0]} -> {q[1]}" for q in quick_queries],
        key="quick_action_select_val",
        on_change=on_quick_action_change
    )
            
    # Chat display container
    chat_container = st.container(height=480)
    
    # Get chat history for current session
    history = session_mgr.get_chat_history(st.session_state["current_session_id"])
    
    with chat_container:
        for msg in history:
            role = msg["role"]
            content = msg["content"]
            html_content = markdown_to_html(content)
            time_formatted = format_timestamp(msg.get("timestamp"))
            time_html = f'<div style="text-align: right; font-size: 0.68rem; margin-top: 4px; color: rgba(255,255,255,0.75);">{time_formatted}</div>' if role == "user" else f'<div style="text-align: right; font-size: 0.68rem; margin-top: 4px; color: var(--text-color); opacity: 0.55;">{time_formatted}</div>'
            
            if role == "user":
                st.markdown(f'<div class="chat-bubble-container user-container"><div class="chat-bubble-new user-bubble-new">{html_content}{time_html}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-container assistant-container"><div class="chat-bubble-new assistant-bubble-new">{html_content}{time_html}</div></div>', unsafe_allow_html=True)
            
    # Chat Input block
    input_key = "chat_input_val"
    if input_key not in st.session_state:
        st.session_state[input_key] = ""
        
    user_input = st.chat_input("พิมพ์สอบถามเกี่ยวกับการกระจายงาน แผนงาน หรือจุดคอขวด...")
    
    # If a button pressed, override user_input
    if st.session_state[input_key]:
        user_input = st.session_state[input_key]
        st.session_state[input_key] = "" # clear state
        
    if user_input:
        now_str = datetime.now().isoformat()
        time_formatted_user = format_timestamp(now_str)
        # Display user input immediately
        with chat_container:
            html_input = markdown_to_html(user_input)
            time_html_user = f'<div style="text-align: right; font-size: 0.68rem; margin-top: 4px; color: rgba(255,255,255,0.75);">{time_formatted_user}</div>'
            st.markdown(f'<div class="chat-bubble-container user-container"><div class="chat-bubble-new user-bubble-new">{html_input}{time_html_user}</div></div>', unsafe_allow_html=True)
            
        with st.spinner("AI Agent กำลังอ่านชีตและประมวลผลวิเคราะห์..."):
            response = agent.ask(st.session_state["current_session_id"], user_input)
            
        # Display assistant response immediately
        with chat_container:
            html_response = markdown_to_html(response)
            time_formatted_assistant = format_timestamp(datetime.now().isoformat())
            time_html_assistant = f'<div style="text-align: right; font-size: 0.68rem; margin-top: 4px; color: var(--text-color); opacity: 0.55;">{time_formatted_assistant}</div>'
            st.markdown(f'<div class="chat-bubble-container assistant-container"><div class="chat-bubble-new assistant-bubble-new">{html_response}{time_html_assistant}</div></div>', unsafe_allow_html=True)
        st.rerun()
