import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.pacientes_service import PacienteService


class ListaScreen(tk.Frame): 
    def __init__(self, parent, controller):
        print("Carregou HOME")
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

        colunas = ("nome", "cpf", "idade")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=10)

        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("cpf", text="CPF")
        self.tabela.heading("idade", text="Idade")

        self.tabela.column("nome", width=180)
        self.tabela.column("cpf", width=120)
        self.tabela.column("idade", width=80)

        self.tabela.place(x=80, y=180)

        tk.Button(self, text="Atualizar Lista", width=18,
                  command=self.carregar).place(x=240, y=360)

        tk.Button(self, text="Voltar", width=10,
                  command=lambda: controller.show_screen("home")).place(x=10, y=360)

        self.carregar()

    def carregar(self):
        # limpa tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        dados = PacienteService.listar() or []

        # PacienteService.listar() retorna dicionários
        for p in dados:
            self.tabela.insert("", tk.END, values=(p["name"], p["cpf"], p["idade"]))

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
