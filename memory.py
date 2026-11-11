"""Local SQLite memory for SUPREME AI. Stores chat history and explicit user memories."""
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("SUPREME_MEMORY_DB", Path(__file__).resolve().parent / "data" / "supreme_memory.db"))


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL DEFAULT 'General',
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL CHECK(role IN ('user','assistant')),
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")


def save_memory(content, category="General"):
    content = (content or "").strip()
    if not content:
        return None
    with connect() as conn:
        # Avoid storing the same fact repeatedly.
        row = conn.execute("SELECT id FROM memories WHERE lower(content)=lower(?)", (content,)).fetchone()
        if row:
            return row["id"]
        cur = conn.execute("INSERT INTO memories(category, content) VALUES (?, ?)", (category.strip() or "General", content))
        return cur.lastrowid


def list_memories():
    with connect() as conn:
        rows = conn.execute("SELECT id, category, content, created_at FROM memories ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]


def delete_memory(memory_id):
    with connect() as conn:
        cur = conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
        return cur.rowcount > 0


def clear_memories():
    with connect() as conn:
        conn.execute("DELETE FROM memories")


def add_message(role, content):
    if role not in ("user", "assistant") or not content:
        return
    with connect() as conn:
        conn.execute("INSERT INTO conversations(role, content) VALUES (?, ?)", (role, content[:12000]))
        # Keep the database compact: retain the latest 300 messages.
        conn.execute("DELETE FROM conversations WHERE id NOT IN (SELECT id FROM conversations ORDER BY id DESC LIMIT 300)")


def recent_messages(limit=8):
    with connect() as conn:
        rows = conn.execute("SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in reversed(rows)]


def memory_context(limit=30):
    with connect() as conn:
        rows = conn.execute("SELECT category, content FROM memories ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]


init_db()
