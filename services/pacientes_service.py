from core.repository import PacienteRepository

class PacienteService:

    @staticmethod
    def cadastrar(dados):
        existente = PacienteRepository.buscar_por_cpf(dados["cpf"])
        if existente:
            print("❌ Paciente já cadastrado!")
            return

        PacienteRepository.inserir(dados)
        print("✔ Paciente cadastrado com sucesso.")

    @staticmethod
    def listar():
        pacientes = PacienteRepository.listar()
        if not pacientes:
            print("⚠ Nenhum paciente cadastrado.")
            return

        for p in pacientes:
            print(p)

    @staticmethod
    def atualizar(cpf, campo, valor):
        if not PacienteRepository.buscar_por_cpf(cpf):
            print("❌ CPF não encontrado.")
            return

        PacienteRepository.atualizar(cpf, campo, valor)
        print("✔ Registro atualizado.")

    @staticmethod
    def excluir(cpf):
        if not PacienteRepository.buscar_por_cpf(cpf):
            print("❌ CPF não encontrado.")
            return

        PacienteRepository.excluir(cpf)
        print("✔ Paciente removido.")
