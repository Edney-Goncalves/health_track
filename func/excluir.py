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