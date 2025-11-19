import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.pacientes_service import PacienteService


class ListaScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.build_logo()

        tk.Label(
            self,
            text="Lista de Pacientes",
            font=("Verdana", 12, "bold"),
            fg="blue",
            bg="white"
        ).place(x=220, y=140)

        # Definição das colunas exibidas
        colunas = ("name", "cpf", "age")

        self.tabela = ttk.Treeview(
            self,
            columns=colunas,
            show="headings",
            height=10
        )

        # Cabeçalhos
        self.tabela.heading("name", text="Nome")
        self.tabela.heading("cpf", text="CPF")
        self.tabela.heading("age", text="Idade")

        # Largura das colunas
        self.tabela.column("name", width=180)
        self.tabela.column("cpf", width=120)
        self.tabela.column("age", width=80)

        self.tabela.place(x=80, y=180)

        # Botões
        tk.Button(
            self,
            text="Atualizar Lista",
            width=18,
            command=self.carregar
        ).place(x=240, y=360)

        tk.Button(
            self,
            text="Voltar",
            width=10,
            command=lambda: controller.show_screen("home")
        ).place(x=10, y=360)

        # Carrega inicialmente
        self.carregar()

    def carregar(self):
        """Recarrega a tabela com dados atualizados do banco."""

        # Limpa a tabela antes de inserir novos dados
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Busca lista de pacientes do Service
        dados = PacienteService.listar() or []

        # Preenche a tabela
        for p in dados:
            # Garante que as chaves existem no dicionário
            nome = p.get("name", "")
            cpf = p.get("cpf", "")
            idade = p.get("age", "")

            self.tabela.insert(
                "",
                tk.END,
                values=(nome, cpf, idade)
            )

    def build_logo(self):
        """Carrega a logo (ou texto caso falhe)."""
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except Exception:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
