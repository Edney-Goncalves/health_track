import json
from core.database import db_connection

class PacienteRepository:

    # -------------------------------------
    # LISTAR TODOS
    # -------------------------------------
    @staticmethod
    def listar():
        with db_connection() as (conn, cursor):
            cursor.execute("""
                SELECT 
                    id, name, cpf, rg, age, gender, 
                    health_state, disease_history
                FROM pacient
                ORDER BY id ASC
            """)
            rows = cursor.fetchall()

            return [
                {
                    "id": r[0],
                    "name": r[1],
                    "cpf": r[2],
                    "rg": r[3],
                    "age": r[4],
                    "gender": r[5],
                    "health_state": r[6],
                    "disease_history": r[7],
                }
                for r in rows
            ]

    # -------------------------------------
    # BUSCAR POR CPF
    # -------------------------------------
    @staticmethod
    def buscar_por_cpf(cpf):
        with db_connection() as (conn, cursor):
            cursor.execute("""
                SELECT 
                    id, name, cpf, rg, age, gender, 
                    health_state, disease_history
                FROM pacient
                WHERE cpf = %s
            """, (cpf,))
            r = cursor.fetchone()

            return (
                {
                    "id": r[0],
                    "name": r[1],
                    "cpf": r[2],
                    "rg": r[3],
                    "age": r[4],
                    "gender": r[5],
                    "health_state": r[6],
                    "disease_history": r[7],
                }
                if r else None
            )

    # -------------------------------------
    # INSERIR
    # -------------------------------------
    @staticmethod
    def inserir(dados):
        with db_connection() as (conn, cursor):
            cursor.execute("""
                INSERT INTO pacient (
                    name, cpf, rg, age, gender, health_state, disease_history
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                dados["name"],
                dados["cpf"],
                dados["rg"],
                dados["age"],
                dados["gender"],
                dados["health_state"],
                json.dumps(dados["disease_history"]) 
                    if dados.get("disease_history") 
                    else None
            ))

    # -------------------------------------
    # ATUALIZAR QUALQUER CAMPO
    # -------------------------------------
    @staticmethod
    def atualizar(cpf, campo, valor):
        with db_connection() as (conn, cursor):

            # If updating JSONB
            if campo == "disease_history":
                valor = json.dumps(valor)

            cursor.execute(
                f"UPDATE pacient SET {campo} = %s WHERE cpf = %s",
                (valor, cpf)
            )

    # -------------------------------------
    # EXCLUIR
    # -------------------------------------
    @staticmethod
    def excluir(cpf):
        with db_connection() as (conn, cursor):
            cursor.execute(
                "DELETE FROM pacient WHERE cpf = %s",
                (cpf,)
            )
