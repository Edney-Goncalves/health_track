import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.pacientes_service import listar_pacientes


class ListaScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="white")

        # Logo
        self.build_logo()

        # Título
        tk.Label(
            self,
            text="Lista de Pacientes",
            font=("Verdana", 12, "bold"),
            fg="blue",
            bg="white"
        ).place(x=220, y=140)

        # Tabela
        colunas = ("id", "nome", "cpf", "idade")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=10)

        for col in colunas:
            self.tabela.heading(col, text=col.capitalize())
            self.tabela.column(col, width=130)

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

        # Carrega ao abrir
        self.carregar()

    def carregar(self):
        # Limpar tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Buscar dados
        dados = listar_pacientes()

        # Inserir na tabela
        # Ajuste aqui se o formato da tupla estiver diferente no banco
        for p in dados:
            # Exemplo esperado: (id, nome, cpf, idade)
            self.tabela.insert("", tk.END, values=(p[0], p[1], p[2], p[3]))

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
