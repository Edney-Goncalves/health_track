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