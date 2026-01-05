import sqlite3
import os

DB_PATH = "data"

# Criar banco e tabela se não existir
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                idade INTEGER
            );
        """)
        conn.commit()
        conn.close()

def read_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    dados = cur.execute("SELECT * FROM pacientes").fetchall()
    conn.close()
    return dados

init_db()

try:
    registros = read_data()
    print("=== DADOS DO BANCO ===")
    if registros:
        for r in registros:
            print(r)
    else:
        print("Nenhum registro encontrado.")
except Exception as e:
    print("Erro ao ler o banco:", e)
