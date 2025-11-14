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