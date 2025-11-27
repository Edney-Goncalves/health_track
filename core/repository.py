import sqlite3
from database.connection import get_connection

class PacienteRepository:

    @staticmethod
    def listar():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, cpf, age, rg, gender, health_state, disease_history FROM pacientes ORDER BY name ASC;")
        resultados = cur.fetchall()

        lista = []
        for r in resultados:
            lista.append({
                "name": r[0],
                "cpf": r[1],
                "age": r[2],
                "rg": r[3],
                "gender": r[4],
                "health_state": r[5],
                "disease_history": r[6],
            })
        return lista

    @staticmethod
    def buscar_por_cpf(cpf):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, cpf, age, rg, gender, health_state, disease_history FROM pacientes WHERE cpf = ?;", (cpf,))
        r = cur.fetchone()
        if not r:
            return None
        return {
            "name": r[0],
            "cpf": r[1],
            "age": r[2],
            "rg": r[3],
            "gender": r[4],
            "health_state": r[5],
            "disease_history": r[6],
        }

    @staticmethod
    def inserir(dados):
        conn = get_connection()
        cur = conn.cursor()
        query = """
            INSERT INTO pacientes (name, cpf, age, rg, gender, health_state, disease_history)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(query, (
            dados["name"],
            dados["cpf"],
            dados["age"],
            dados["rg"],
            dados["gender"],
            dados["health_state"],
            str(dados["disease_history"])  # armazenado como texto
        ))
        conn.commit()
        return cur.lastrowid

    @staticmethod
    def atualizar(cpf, campo, valor):
        conn = get_connection()
        cur = conn.cursor()
        query = f"UPDATE pacientes SET {campo} = ? WHERE cpf = ?;"
        cur.execute(query, (valor, cpf))
        conn.commit()
        return cur.rowcount

    @staticmethod
    def excluir(cpf):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM pacientes WHERE cpf = ?;", (cpf,))
        conn.commit()
        return cur.rowcount
