import pytest
import mcp_server

# Force mock database usage and offline agent responding in tests
mcp_server.get_google_sheets_service = lambda: None

import app.agent
app.agent.API_KEY = None

from app.agent import ITRoadmapAgent
from app.session_manager import SessionManager

# Clear cache before running tests
SessionManager().clear_all_caches()

@pytest.fixture
def agent():
    return ITRoadmapAgent()

@pytest.fixture
def session_id():
    return "test-session-123"

def test_agent_task_tracking_pete(agent, session_id):
    query = "ตอนนี้พีททำงานอะไรอยู่"
    response = agent.ask(session_id, query)
    assert "พีท" in response
    assert "Backend" in response
    assert "Doing" in response

def test_agent_progress_deadline_packing(agent, session_id):
    query = "ระบบบรรจุ ทำไปแล้วกี่เปอร์เซ็นต์ คิดว่าจะทำเสร็จทันก่อนส่งงานหรือไม่"
    response = agent.ask(session_id, query)
    assert "บรรจุ" in response or "Onboarding" in response
    assert "75%" in response
    assert "ทีม พี่ป้อม" in response
    assert "เสร็จทัน" in response

def test_agent_specific_task_q(agent, session_id):
    query = "ตอนนี้คิวกำลังพัฒนางาน (doing) อะไรในระบบบรรจุ ช่วย list มาให้หน่อย"
    response = agent.ask(session_id, query)
    assert "คิว" in response
    assert "Backend" in response

def test_agent_idle_check(agent, session_id):
    query = "ตอนนี้ที่ทุกทีมมีใครบ้างที่ไม่มีสถานะงานที่เป็น doing"
    response = agent.ask(session_id, query)
    assert "บาส" in response
    assert "จอย" in response
    assert "กอล์ฟ" in response
    assert "Done" in response
    assert "จัดซื้อ" in response

def test_agent_bottleneck_summary(agent, session_id):
    query = "มีระบบไหนของทีมไหนบ้างที่มีสถานะเป็น Paused หรือ Backlog และมีหมายเหตุแจ้งว่าอะไร?"
    response = agent.ask(session_id, query)
    assert "งบประมาณรายได้" in response or "Revenue Budgeting" in response
    assert "ปีงบประมาณ 70" in response
    assert "ST03" in response
    assert "จัดซื้อ" in response
