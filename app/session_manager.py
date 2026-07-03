import sqlite3
import os
import json
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "sessions.db")

def init_db():
    """Initializes the SQLite database schema if it doesn't exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP
        )
    """)
    
    # Create chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(session_id)
        )
    """)
    
    # Create sheets data cache table (for caching GSheets to prevent API rate limits)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sheet_cache (
            team_name TEXT,
            sheet_name TEXT,
            data_json TEXT,
            updated_at TIMESTAMP,
            PRIMARY KEY (team_name, sheet_name)
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()

class SessionManager:
    def __init__(self):
        self.db_path = DB_PATH
        
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
        
    def create_session(self, session_id: str, title: str = "New Session") -> bool:
        """Creates a new session in the database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO sessions (session_id, title, created_at) VALUES (?, ?, ?)",
                (session_id, title, datetime.now().isoformat())
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Already exists
        finally:
            conn.close()
            
    def get_all_sessions(self) -> list[dict]:
        """Returns all sessions sorted by creation time."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT session_id, title, created_at FROM sessions ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{"session_id": r[0], "title": r[1], "created_at": r[2]} for r in rows]
        
    def add_message(self, session_id: str, role: str, content: str):
        """Adds a chat message to a session's history."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, role, content, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        
    def get_chat_history(self, session_id: str) -> list[dict]:
        """Fetches the complete chat history for a session."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content, timestamp FROM chat_history WHERE session_id = ? ORDER BY id ASC",
            (session_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in rows]
        
    def clear_session_chat(self, session_id: str):
        """Clears chat history for a given session."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

    def set_sheet_cache(self, team_name: str, sheet_name: str, data: list):
        """Caches sheet data as serialized JSON to prevent API rate limit."""
        conn = self._get_connection()
        cursor = conn.cursor()
        data_json = json.dumps(data, ensure_ascii=False)
        cursor.execute("""
            INSERT OR REPLACE INTO sheet_cache (team_name, sheet_name, data_json, updated_at)
            VALUES (?, ?, ?, ?)
        """, (team_name, sheet_name, data_json, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
    def get_sheet_cache(self, team_name: str, sheet_name: str) -> list:
        """Retrieves cached sheet data. Returns None if cache doesn't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT data_json FROM sheet_cache WHERE team_name = ? AND sheet_name = ?",
            (team_name, sheet_name)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            try:
                return json.loads(row[0])
            except Exception:
                return None
        return None
        
    def clear_all_caches(self):
        """Clears GSheets cache database entirely."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sheet_cache")
        conn.commit()
        conn.close()
