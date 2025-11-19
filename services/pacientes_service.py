from core.repository import PacienteRepository

class PacienteService:

    # -------------------------------------
    # CADASTRAR PACIENTE
    # -------------------------------------
    @staticmethod
    def cadastrar(dados):
        existente = PacienteRepository.buscar_por_cpf(dados["cpf"])
        if existente:
            raise Exception("Paciente já cadastrado!")

        PacienteRepository.inserir({
            "name": dados["name"],
            "cpf": dados["cpf"],
            "rg": dados["rg"],
            "age": dados["age"],
            "gender": dados["gender"],
            "health_state": dados["health_state"],
            "disease_history": dados.get("disease_history"),
        })

    # -------------------------------------
    # LISTAR
    # -------------------------------------
    @staticmethod
    def listar():
        pacientes = PacienteRepository.listar()
        return pacientes if pacientes else []

    # -------------------------------------
    # ATUALIZAR
    # -------------------------------------
    @staticmethod
    def atualizar(cpf, campo, valor):
        if not PacienteRepository.buscar_por_cpf(cpf):
            raise Exception("CPF não encontrado.")

        PacienteRepository.atualizar(cpf, campo, valor)

    # -------------------------------------
    # EXCLUIR
    # -------------------------------------
    @staticmethod
    def excluir(cpf):
        if not PacienteRepository.buscar_por_cpf(cpf):
            raise Exception("CPF não encontrado.")

        PacienteRepository.excluir(cpf)
