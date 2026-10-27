import sqlite3
import re

DB_FILE = "tickets.db"

def _connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'New',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """)
    return conn

def redact(text):
    return re.sub(
        r"\b(password|passcode|pin|code)\s*(?:(?:is|its|it's)\b|[:=])\s*"
        r"(?!(?:not|working|wrong|incorrect|expired|locked|invalid|correct|too|very|weak|easy|about|the|a|an)\b)\S+",
        r"\1 [removed]",
        text,
        flags=re.IGNORECASE,
    )

def create_ticket(question):
    question = redact(question)
    conn = _connect()
    cur = conn.execute("INSERT INTO tickets (question) VALUES (?)", (question,))
    conn.commit()
    ticket_id = cur.lastrowid
    conn.close()
    return ticket_id

def list_tickets():
    conn = _connect()
    rows = conn.execute("SELECT id, question, status, created_at FROM tickets ORDER BY id").fetchall()
    conn.close()
    return rows