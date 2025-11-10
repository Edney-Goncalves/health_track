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