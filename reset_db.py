import sqlite3

# 🔥 MUITO IMPORTANTE:
# Aqui você coloca o nome EXATO do arquivo de banco
# Se seu projeto usa "database.db", deixe como está.
# Se usa "data.db", troque aqui antes de rodar.

DB_FILE = "data.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

print("Apagando tabela 'pacientes' se existir...")
cur.execute("DROP TABLE IF EXISTS pacientes;")

print("Criando nova tabela...")
cur.execute("""
CREATE TABLE pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    rg TEXT,
    gender TEXT,
    health_state TEXT,
    disease_history TEXT
);
""")

conn.commit()
conn.close()

print("✔ Banco recriado com sucesso!")
