from core.database import initialize_database
from services.pacientes_service import PacienteService


def menu():
    print("""
==== SISTEMA DE PACIENTES ====
1 - Cadastrar
2 - Listar
3 - Atualizar
4 - Excluir
0 - Sair
""")

def main():
    initialize_database()

    while True:
        menu()
        op = input("Escolha: ")

        if op == "1":
            dados = {
                "name": input("Nome: "),
                "cpf": input("CPF: "),
                "rg": input("RG: "),
                "health_state": input("Estado de saúde: "),
                "age": int(input("Idade: ")),
                "gender": input("Gênero: "),
                "disease_history": None
            }
            PacienteService.cadastrar(dados)

        elif op == "2":
            PacienteService.listar()

        elif op == "3":
            cpf = input("CPF: ")
            campo = input("Campo para alterar: ")
            valor = input("Novo valor: ")
            PacienteService.atualizar(cpf, campo, valor)

        elif op == "4":
            cpf = input("CPF: ")
            PacienteService.excluir(cpf)

        elif op == "0":
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
