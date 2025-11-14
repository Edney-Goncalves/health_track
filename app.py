# ========================================
# UNIVERSIDADE DE MOGI DAS CRUZES - UMC
# Professor: Luiz Carlos dos Santos Filho
# Programa: Mini-Projeto de Software Básico (versão PostgreSQL)
# Desenvolvido por: Edney Leandro Gonçalves, Gustavo Seiji, João Pedro Duo,
#                   João Pedro Perez e Willi Hasman
# Data: 03/12/2025
# ========================================


import os
import time
import json
import psycopg2
from psycopg2 import errors
from dotenv import load_dotenv

# ====================================================
# CONFIGURAÇÃO DE CONEXÃO (usa variáveis do .env)
# ====================================================
load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def conectar():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    # Cria a tabela se não existir
    cur.execute("""
		CREATE TABLE IF NOT EXISTS pacient (
			id SERIAL PRIMARY KEY,
			name VARCHAR(100) NOT NULL,
			cpf VARCHAR(11) UNIQUE NOT NULL,
			rg VARCHAR(20) UNIQUE NOT NULL,
			health_state TEXT,
			age INTEGER NOT NULL,
			gender VARCHAR(20),
			disease_history JSONB
		);
	""")

    conn.commit()
    return conn, cur


# ====================================================
# FUNÇÕES AUXILIARES
# ====================================================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPressione ENTER para continuar...")


# ====================================================
# CRUD
# ====================================================
def cadastrar():
    limpar_tela()
    print("=== CADASTRAR PACIENTE ===")

    conn, cur = conectar()

    name = input("Nome: ").strip()
    cpf = input("CPF (somente números): ").strip()
    rg = input("RG: ").strip()
    health_state = input("Estado de saúde: ").strip()
    age = input("Idade: ").strip()
    gender = input("Gênero: ").strip()
    disease_history = input("Histórico de doenças (separe por vírgula): ").strip()

    if not name or not cpf or not rg or not age:
        print("❌ Campos obrigatórios não podem ficar vazios!")
        conn.close()
        pausar()
        return

    if not age.isdigit():
        print("❌ Idade deve ser um número inteiro!")
        conn.close()
        pausar()
        return

    # Converte histórico para JSON
    lista_historico = [item.strip() for item in disease_history.split(",")] if disease_history else []
    historico_json = json.dumps(lista_historico)

    try:
        cur.execute("""
            INSERT INTO pacient (name, cpf, rg, health_state, age, gender, disease_history)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (name, cpf, rg, health_state, int(age), gender, historico_json))
        conn.commit()
        print("✅ Paciente cadastrado com sucesso!")
    except errors.UniqueViolation:
        print("❌ CPF ou RG já cadastrado!")
        conn.rollback()
    except Exception as e:
        print(f"❌ Erro ao cadastrar: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    pausar()


def listar():
    limpar_tela()
    print("=== LISTAR PACIENTE ===")

    conn, cur = conectar()
    cur.execute("SELECT * FROM pacient ORDER BY id;")
    pacient = cur.fetchall()

    if not pacient:
        print("Nenhum paciente encontrado.")
    else:
        for c1 in pacient:
            print(f"ID: {c1[0]} | Nome: {c1[1]} | CPF: {c1[2]} | RG: {c1[3]} | Idade: {c1[5]} | Gênero: {c1[6]}")

    cur.close()
    conn.close()
    pausar()


def atualizar():
    limpar_tela()
    print("=== ATUALIZAR PACIENTE ===")
    conn, cur = conectar()
    id_busca = input("Informe o ID do paciente: ").strip()

    cur.execute("SELECT * FROM pacient WHERE id = %s;", (id_busca,))
    paciente = cur.fetchone()

    if not paciente:
        print("❌ Paciente não encontrado!")
        cur.close()
        conn.close()
        pausar()
        return

    name = input(f"Novo name ({paciente[1]}): ").strip() or paciente[1]
    health_state = input(f"Novo estado de saúde ({paciente[4]}): ").strip() or paciente[4]
    age = input(f"Nova age ({paciente[5]}): ").strip() or paciente[5]
    gender = input(f"Novo gênero ({paciente[6]}): ").strip() or paciente[6]
    disease_history = input(f"Novo histórico (JSON) ({paciente[7]}): ").strip() or json.dumps(paciente[7])

    try:
        cur.execute("""
            UPDATE pacient
            SET name=%s, health_state=%s, age=%s, gender=%s, disease_history=%s
            WHERE id=%s;
        """, (name, health_state, age, gender, disease_history, id_busca))
        conn.commit()
        print("✅ Paciente atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    pausar()


def excluir():
    limpar_tela()
    print("=== EXCLUIR PACIENTE ===")
    conn, cur = conectar()
    id_busca = input("Informe o ID do paciente para excluir: ").strip()

    cur.execute("DELETE FROM pacient WHERE id = %s;", (id_busca,))
    conn.commit()

    if cur.rowcount > 0:
        print("✅ Paciente excluído com sucesso!")
    else:
        print("❌ Paciente não encontrado!")

    cur.close()
    conn.close()
    pausar()


def relatorio():
    limpar_tela()
    print("=== RELATÓRIO DE PESQUISA ===")
    termo = input("Buscar por name ou CPF: ").strip().lower()

    conn, cur = conectar()
    cur.execute("""
        SELECT * FROM pacient
        WHERE LOWER(name) LIKE %s OR LOWER(cpf) LIKE %s;
    """, (f"%{termo}%", f"%{termo}%"))
    resultados = cur.fetchall()

    cur.close()
    conn.close()

    if resultados:
        print("\nResultados encontrados:")
        for r in resultados:
            print(f"ID: {r[0]} | Nome: {r[1]} | CPF: {r[2]} | Estado: {r[4]} | Idade: {r[5]} | Gênero: {r[6]}")
        print(f"\nTotal de registros: {len(resultados)}")
    else:
        print("Nenhum paciente encontrado.")

    pausar()


# ====================================================
# MENU PRINCIPAL
# ====================================================
def menu():
    while True:
        limpar_tela()
        print("=========================================")
        print("       HEALTH TRACK ")
        print("O sistema que cuida de você")
        print("=========================================")
        print("1 - Cadastrar Paciente")
        print("2 - Listar Paciente")
        print("3 - Atualizar Paciente")
        print("4 - Excluir Paciente")
        print("5 - Relatório de pesquisa")
        print("0 - Sair")
        print("=========================================")

        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1": cadastrar()
            case "2": listar()
            case "3": atualizar()
            case "4": excluir()
            case "5": relatorio()
            case "0":
                print("Saindo...")
                time.sleep(1)
                break
            case _:
                print("❌ Opção inválida!")
                time.sleep(1)


if __name__ == "__main__":
    menu()
