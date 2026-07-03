import os
import json
import re
from mcp.server.fastmcp import FastMCP
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mcp = FastMCP("excel-roadmap-server")

# Path to service account file and mock database
CREDENTIALS_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "credentials.json")
MOCK_DB_PATH = os.path.join(os.path.dirname(__file__), "database", "mock_roadmap.json")

# Map of team names to environment variable names for URLs
TEAM_URL_ENV_MAP = {
    "ทีม พีท เจมส์ หวาน": "GOOGLE_SHEET_PDM_URL",
    "ทีม ป้อม อาร์ต นัท บี": "GOOGLE_SHEET_KAI_URL",
    "ทีม เจน กิฟต์ โต้ง": "GOOGLE_SHEET_SU_URL",
    "ทีม คิว กอล์ฟ นนท์": "GOOGLE_SHEET_Q_URL",
    "ทีม แพร แบงค์ บาส": "GOOGLE_SHEET_FARBOOKMARK_URL",
    "ทีม นัท จอย": "GOOGLE_SHEET_OEITUK_URL",
    "ทีม พี่ป้อม": "GOOGLE_SHEET_JIRAPAH_URL"
}

def extract_spreadsheet_id(url: str) -> str:
    """Extracts spreadsheet ID from a Google Sheet URL."""
    if not url:
        return ""
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
    return match.group(1) if match else ""

def get_google_sheets_service():
    """Initializes Google Sheets API service if credentials exist."""
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=scopes
        )
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f"Error initializing Google API: {e}")
        return None

def read_mock_data(team_name: str, sheet_name: str = None) -> list:
    """Reads project data from local mock JSON database."""
    if not os.path.exists(MOCK_DB_PATH):
        return []
    try:
        with open(MOCK_DB_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
        
        team_data = db.get(team_name)
        if not team_data:
            return []
        
        if sheet_name:
            return team_data.get(sheet_name, [])
        return team_data
    except Exception as e:
        print(f"Error reading mock database: {e}")
        return []

def read_google_sheet(spreadsheet_id: str, range_name: str) -> list[list]:
    """Reads values from a Google Sheet range using API."""
    service = get_google_sheets_service()
    if not service:
        raise ValueError("Google Sheets Service not initialized")
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    return result.get('values', [])

@mcp.tool()
def get_all_teams() -> str:
    """Returns a list of all configured team names in the system."""
    return json.dumps(list(TEAM_URL_ENV_MAP.keys()), ensure_ascii=False)

def map_project_headers(headers: list) -> dict:
    mapping = {}
    for idx, h in enumerate(headers):
        h_str = str(h).strip().lower()
        if h_str == "sheet" or "รหัส" in h_str:
            mapping["รหัส Project"] = idx
        elif "ระบบ" in h_str:
            mapping["ชื่อระบบ"] = idx
        elif "หัวหน้า" in h_str:
            mapping["หัวหน้าทีม"] = idx
        elif "ผู้ร่วมทีม" in h_str:
            mapping["ผู้ร่วมทีม"] = idx
        elif "เริ่ม" in h_str:
            mapping["วันที่เริ่มต้น"] = idx
        elif "สิ้นสุด" in h_str:
            mapping["วันที่สิ้นสุด"] = idx
        elif "กำหนดส่ง" in h_str or "ส่งงาน" in h_str:
            mapping["กำหนดส่งงาน"] = idx
        elif "สถานะ" in h_str:
            mapping["สถานะของ Project"] = idx
        elif "คืบหน้า" in h_str or "%" in h_str:
            mapping["เปอร์เซ็นต์ความคืบหน้าของ Project"] = idx
        elif "หมายเหตุ" in h_str:
            mapping["หมายเหตุ"] = idx
    return mapping

@mcp.tool()
def fetch_project_summary(team_name: str) -> str:
    """Fetches the project roadmap overview (from 'Project' sheet) for a specific team."""
    env_var = TEAM_URL_ENV_MAP.get(team_name)
    url = os.getenv(env_var) if env_var else None
    spreadsheet_id = extract_spreadsheet_id(url)
    
    # Try Google API first
    if spreadsheet_id:
        try:
            # Read columns A to O (index 0 to 14) to catch all possible header columns
            raw_rows = read_google_sheet(spreadsheet_id, "Project!A:O")
            if raw_rows and len(raw_rows) > 0:
                headers = raw_rows[0]
                header_map = map_project_headers(headers)
                results = []
                for r in raw_rows[1:]:
                    row_dict = {}
                    # Build standard keys based on dynamic index mappings
                    for std_key, col_idx in header_map.items():
                        if col_idx < len(r):
                            row_dict[std_key] = r[col_idx].strip()
                        else:
                            row_dict[std_key] = ""
                    # Default values for missing keys to maintain consistency
                    for std_key in ["รหัส Project", "ชื่อระบบ", "หัวหน้าทีม", "ผู้ร่วมทีม", "วันที่เริ่มต้น", "วันที่สิ้นสุด", "กำหนดส่งงาน", "สถานะของ Project", "เปอร์เซ็นต์ความคืบหน้าของ Project", "หมายเหตุ"]:
                        if std_key not in row_dict:
                            row_dict[std_key] = ""
                    results.append(row_dict)
                return json.dumps(results, ensure_ascii=False)
        except Exception as e:
            print(f"Google API reading failed, falling back to mock: {e}")
            
    # Fallback to mock
    mock_data = read_mock_data(team_name, "Project")
    return json.dumps(mock_data, ensure_ascii=False)

@mcp.tool()
def fetch_st_detail(team_name: str, st_code: str) -> str:
    """Fetches the micro task details for a specific project sheet (e.g. ST1, ST2) of a team."""
    normalized_code = st_code
    match = re.match(r"ST0*(\d+)", st_code, re.IGNORECASE)
    if match:
        normalized_code = f"ST{match.group(1)}"
        
    env_var = TEAM_URL_ENV_MAP.get(team_name)
    url = os.getenv(env_var) if env_var else None
    spreadsheet_id = extract_spreadsheet_id(url)
    
    if spreadsheet_id:
        try:
            # Read columns A to J to cover descriptions, owners, and statuses
            raw_rows = read_google_sheet(spreadsheet_id, f"{normalized_code}!A:J")
            if raw_rows and len(raw_rows) > 0:
                headers = [str(x).strip().lower() for x in raw_rows[0]]
                
                # Dynamic matching of column indices
                desc_indices = [idx for idx, h in enumerate(headers) if any(x in h for x in ["module", "feature", "รายละเอียด", "งานย่อย", "กิจกรรม"])]
                resp_idx = next((idx for idx, h in enumerate(headers) if any(x in h for x in ["ผู้รับผิดชอบ", "รับผิดชอบ", "assign", "member"])), -1)
                status_idx = next((idx for idx, h in enumerate(headers) if "สถานะ" in h), -1)
                remark_idx = next((idx for idx, h in enumerate(headers) if any(x in h for x in ["หมายเหตุ", "remarks", "deadline", "กำหนดส่ง"])), -1)
                
                results = []
                for r in raw_rows[1:]:
                    # Extract description from first non-empty mapped description column
                    task_desc = ""
                    for d_idx in desc_indices:
                        if d_idx < len(r) and r[d_idx].strip():
                            task_desc = r[d_idx].strip()
                            break
                    
                    row_dict = {
                        "งานย่อย/กิจกรรม": task_desc,
                        "ผู้รับผิดชอบ": r[resp_idx].strip() if (resp_idx != -1 and resp_idx < len(r)) else "",
                        "สถานะ": r[status_idx].strip() if (status_idx != -1 and status_idx < len(r)) else "",
                        "หมายเหตุ": r[remark_idx].strip() if (remark_idx != -1 and remark_idx < len(r)) else ""
                    }
                    # Clean up status (standardize back to Doing/Done/To Do)
                    clean_status = row_dict["สถานะ"]
                    if "doing" in clean_status.lower() or "กำลังทำ" in clean_status:
                        clean_status = "Doing"
                    elif "done" in clean_status.lower() or "เสร็จ" in clean_status:
                        clean_status = "Done"
                    elif "to do" in clean_status.lower() or "รอ" in clean_status or "ค้าง" in clean_status:
                        clean_status = "To Do"
                    row_dict["สถานะ"] = clean_status
                    
                    if row_dict["งานย่อย/กิจกรรม"] or row_dict["ผู้รับผิดชอบ"]:
                        results.append(row_dict)
                return json.dumps(results, ensure_ascii=False)
        except Exception as e:
            print(f"Google API reading failed for {normalized_code}, falling back to mock: {e}")
            
    mock_data = read_mock_data(team_name, normalized_code)
    return json.dumps(mock_data, ensure_ascii=False)

@mcp.tool()
def update_project_status(team_name: str, st_code: str, row_index: int, new_status: str) -> str:
    """Updates the status of a sub-task in Google Sheets (or mock database) for a project."""
    normalized_code = st_code
    match = re.match(r"ST0*(\d+)", st_code, re.IGNORECASE)
    if match:
        normalized_code = f"ST{match.group(1)}"
        
    env_var = TEAM_URL_ENV_MAP.get(team_name)
    url = os.getenv(env_var) if env_var else None
    spreadsheet_id = extract_spreadsheet_id(url)
    
    if spreadsheet_id:
        try:
            service = get_google_sheets_service()
            if service:
                # Typically status is in Column C (3rd column, index 2)
                # row_index is 1-indexed (and row 1 is header, so row_index 2 is the 1st data row)
                range_to_update = f"{normalized_code}!C{row_index}"
                body = {'values': [[new_status]]}
                service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=range_to_update,
                    valueInputOption="RAW",
                    body=body
                ).execute()
                return f"Successfully updated task status to '{new_status}' in Google Sheets cell {range_to_update}."
        except Exception as e:
            print(f"Google API update failed, falling back to mock: {e}")
            
    # Mock database update
    if os.path.exists(MOCK_DB_PATH):
        try:
            with open(MOCK_DB_PATH, "r", encoding="utf-8") as f:
                db = json.load(f)
            
            team_data = db.get(team_name)
            if team_data and normalized_code in team_data:
                tasks = team_data[normalized_code]
                # Adjust index: row_index - 2 is the index in array (assuming row 1 is headers)
                arr_idx = row_index - 2
                if 0 <= arr_idx < len(tasks):
                    tasks[arr_idx]["สถานะ"] = new_status
                    
                    # Update progress in Project overview tab as well (Done / Total)
                    done_count = sum(1 for t in tasks if t["สถานะ"] == "Done")
                    total_count = len(tasks)
                    projects = team_data.get("Project", [])
                    for p in projects:
                        if p.get("รหัส Project") == normalized_code:
                            p["จำนวนงานที่เสร็จแล้ว Done"] = done_count
                            p["จำนวนงานทั้งหมด"] = total_count
                            progress_pct = f"{round((done_count / total_count) * 100, 2)}%" if total_count > 0 else "0%"
                            p["เปอร์เซ็นต์ความคืบหน้าของ Project"] = progress_pct
                    
                    with open(MOCK_DB_PATH, "w", encoding="utf-8") as f:
                        json.dump(db, f, ensure_ascii=False, indent=2)
                    return f"Successfully updated task status to '{new_status}' in Mock Database at index {arr_idx}."
        except Exception as e:
            return f"Failed to update task status in mock database: {e}"
            
    return "Failed to update project status. Spreadsheet not found."

if __name__ == "__main__":
    mcp.run()
