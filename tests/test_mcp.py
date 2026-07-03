import pytest
import json
import mcp_server

# Force mock database usage in tests by returning None for Google service
mcp_server.get_google_sheets_service = lambda: None

from app.session_manager import SessionManager
SessionManager().clear_all_caches()

from mcp_server import get_all_teams, fetch_project_summary, fetch_st_detail, update_project_status

def test_mcp_get_all_teams():
    teams_json = get_all_teams()
    teams = json.loads(teams_json)
    assert len(teams) == 7
    assert "ทีม พีท เจมส์ หวาน" in teams
    assert "ทีม พี่ป้อม" in teams

def test_mcp_fetch_project_summary():
    summary_json = fetch_project_summary("ทีม พีท เจมส์ หวาน")
    summary = json.loads(summary_json)
    assert len(summary) >= 2
    assert summary[0]["รหัส Project"] == "ST1"
    assert "ระบบอนุมัติปฏิบัติงาน" in summary[0]["ชื่อระบบ"]
    assert summary[0]["หัวหน้าทีม"] == "พีท"

def test_mcp_fetch_st_detail():
    st_detail_json = fetch_st_detail("ทีม พีท เจมส์ หวาน", "ST1")
    st_detail = json.loads(st_detail_json)
    assert len(st_detail) >= 3
    assert st_detail[0]["งานย่อย/กิจกรรม"] == "ออกแบบฐานข้อมูล"
    assert st_detail[0]["ผู้รับผิดชอบ"] == "พีท"
    assert st_detail[0]["สถานะ"] == "Done"

def test_mcp_update_project_status():
    # Update status in mock and verify it returns success
    msg = update_project_status("ทีม พีท เจมส์ หวาน", "ST1", 4, "Done") # index 4 corresponds to data index 2
    assert "Successfully updated" in msg
    
    # Reload detail to verify
    st_detail_json = fetch_st_detail("ทีม พีท เจมส์ หวาน", "ST1")
    st_detail = json.loads(st_detail_json)
    assert st_detail[2]["สถานะ"] == "Done"
    
    # Reset back to Doing for future consistency
    update_project_status("ทีม พีท เจมส์ หวาน", "ST1", 4, "Doing")
