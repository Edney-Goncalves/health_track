from core.repository import PacienteRepository

class PacienteServiceClass:
    def __init__(self):
        self.repo = PacienteRepository()
        self.repo.create_table()  # garante criação imediata

    def adicionar(self, name, cpf, age):
        return self.repo.adicionar(name, cpf, age)

    def listar(self):
        return self.repo.listar()

    def atualizar(self, cpf, campo, valor):
        return self.repo.atualizar(cpf, campo, valor)

    def excluir(self, cpf):
        return self.repo.excluir(cpf)

# INSTÂNCIA ÚNICA
PacienteService = PacienteServiceClass()
