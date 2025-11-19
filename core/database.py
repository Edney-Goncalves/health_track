import psycopg2
from psycopg2 import Error
from contextlib import contextmanager
from config.env import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


TABLE_SQL = """
CREATE TABLE IF NOT EXISTS pacient(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    rg VARCHAR(20) NOT NULL UNIQUE,
    age SMALLINT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    health_state VARCHAR(255) NOT NULL,
    disease_history JSONB
);
"""

def initialize_database():
    try:
        with psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(TABLE_SQL)
            conn.commit()
    except Error as e:
        print("Erro ao inicializar o banco:", e)
        raise


@contextmanager
def db_connection():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            
        )
        cur = conn.cursor()
        yield conn, cur
        conn.commit()

    except Error as e:
        if conn:
            conn.rollback()
        print("Erro no banco:", e)
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
