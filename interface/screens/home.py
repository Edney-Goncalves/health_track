import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class HomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(style="Home.TFrame")
        self.build_logo()

        # Título
        titulo = tk.Label(
            self,
            text="Selecione uma das opções abaixo",
            font=("Verdana", 10, "italic", "bold"),
            fg="blue",
            bg="white"
        )
        titulo.place(x=190, y=130)

        # Botões principais
        self.botao("Cadastrar Paciente", 180, lambda: controller.show_screen("cadastro"))
        self.botao("Listar Paciente", 220, lambda: controller.show_screen("lista"))
        self.botao("Atualizar Paciente", 260, lambda: controller.show_screen("editar"))
        self.botao("Excluir Paciente", 300, lambda: controller.show_screen("excluir"))
        self.botao("Relatório de pesquisa", 340, lambda: controller.show_screen("relatorio"))

        # Botão sair
        tk.Button(
            self,
            text="Finalizar o Sistema",
            width=15,
            command=self.controller.root.destroy
        ).place(x=480, y=360)

    # ------- Componentes reutilizáveis -------
    def botao(self, texto, y, comando):
        tk.Button(self, text=texto, width=18, command=comando).place(x=240, y=y)

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except Exception:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
