import json
import os

class PacienteRepository:
    FILE_PATH = "pacientes.json"

    @staticmethod
    def carregar():
        if not os.path.exists(PacienteRepository.FILE_PATH):
            return []

        with open(PacienteRepository.FILE_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def salvar(lista):
        with open(PacienteRepository.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)

    @staticmethod
    def adicionar(paciente):
        lista = PacienteRepository.carregar()
        lista.append(paciente)
        PacienteRepository.salvar(lista)

    @staticmethod
    def atualizar(cpf, dados):
        lista = PacienteRepository.carregar()
        for p in lista:
            if p["cpf"] == cpf:
                p.update(dados)
                PacienteRepository.salvar(lista)
                return True
        return False

    @staticmethod
    def remover(cpf):
        lista = PacienteRepository.carregar()
        nova_lista = [p for p in lista if p["cpf"] != cpf]

        if len(lista) == len(nova_lista):
            return False

        PacienteRepository.salvar(nova_lista)
        return True

    @staticmethod
    def buscar(cpf):
        lista = PacienteRepository.carregar()
        for p in lista:
            if p["cpf"] == cpf:
                return p
        return None

    @staticmethod
    def listar():
        return PacienteRepository.carregar()
