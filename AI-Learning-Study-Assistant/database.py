import sqlite3
from datetime import datetime

DB_NAME = "study_assistant.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            note TEXT,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            score INTEGER,
            total INTEGER,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_memory(topic, note):
    conn = get_connection()
    conn.execute(
        "INSERT INTO memory(topic, note, created_at) VALUES (?, ?, ?)",
        (topic, note, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def save_quiz_result(topic, score, total):
    conn = get_connection()
    conn.execute(
        "INSERT INTO quiz_results(topic, score, total, created_at) VALUES (?, ?, ?, ?)",
        (topic, score, total, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_progress():
    conn = get_connection()
    rows = conn.execute(
        "SELECT topic, score, total, created_at FROM quiz_results ORDER BY id DESC"
    ).fetchall()
    memories = conn.execute(
        "SELECT topic, note, created_at FROM memory ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return {"quizzes": rows, "memories": memories}
