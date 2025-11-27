import sqlite3
import os

DB_PATH = "database.db"

def get_connection():
    init_db()
    return sqlite3.connect(DB_PATH)

def init_db():
    # Se o DB já existe, não recria.
    if os.path.exists(DB_PATH):
        return
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            peso REAL,
            altura REAL
        )
    """)

    conn.commit()
    conn.close()
