import sqlite3

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

def create_ticket(question):
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