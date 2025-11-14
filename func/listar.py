ef listar():
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
