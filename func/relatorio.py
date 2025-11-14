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