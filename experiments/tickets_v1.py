print("STEP 23 RUNNING")

import sqlite3

conn = sqlite3.connect("tickets.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'New',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("INSERT INTO tickets (question) VALUES (?)", ("My VPN won't connect",))
conn.commit()

for row in cur.execute("SELECT id, question, status, created_at FROM tickets"):
    print(row)

conn.close()