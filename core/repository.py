from core.database import db_connection

class PacienteRepository:

    @staticmethod
    def inserir(paciente):
        with db_connection() as (conn, cur):
            cur.execute("""
                INSERT INTO pacient (name, cpf, rg, health_state, age, gender, disease_history)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                paciente["name"],
                paciente["cpf"],
                paciente["rg"],
                paciente["health_state"],
                paciente["age"],
                paciente["gender"],
                paciente["disease_history"]
            ))

    @staticmethod
    def listar():
        with db_connection() as (conn, cur):
            cur.execute("SELECT * FROM pacient")
            return cur.fetchall()

    @staticmethod
    def buscar_por_cpf(cpf):
        with db_connection() as (conn, cur):
            cur.execute("SELECT * FROM pacient WHERE cpf = %s", (cpf,))
            return cur.fetchone()

    @staticmethod
    def atualizar(cpf, campo, novo_valor):
        with db_connection() as (conn, cur):
            cur.execute(f"UPDATE pacient SET {campo} = %s WHERE cpf = %s", (novo_valor, cpf))

    @staticmethod
    def excluir(cpf):
        with db_connection() as (conn, cur):
            cur.execute("DELETE FROM pacient WHERE cpf = %s", (cpf,))
