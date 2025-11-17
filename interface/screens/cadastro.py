import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.pacientes_service import PacienteService



class CadastroScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(style="Home.TFrame")
        self.build_logo()

        # Título
        tk.Label(
            self,
            text="Cadastro de Paciente",
            font=("Verdana", 12, "bold"),
            fg="blue",
            bg="white"
        ).place(x=220, y=140)

        # Campo Nome
        tk.Label(self, text="Nome", bg="white").place(x=180, y=190)
        self.nome = tk.Entry(self, width=25)
        self.nome.place(x=260, y=190)

        # Campo CPF
        tk.Label(self, text="CPF", bg="white").place(x=180, y=220)
        self.cpf = tk.Entry(self, width=25)
        self.cpf.place(x=260, y=220)

        # Campo Idade
        tk.Label(self, text="Idade", bg="white").place(x=180, y=250)
        self.idade = tk.Entry(self, width=25)
        self.idade.place(x=260, y=250)

        # Botões
        tk.Button(
            self,
            text="Salvar",
            width=18,
            command=self.salvar
        ).place(x=240, y=300)

        tk.Button(
            self,
            text="Voltar",
            width=10,
            command=lambda: controller.show_screen("home")
        ).place(x=10, y=360)

    def salvar(self):
        dados = {
            "name": self.nome.get(),
            "cpf": self.cpf.get(),
            "age": self.idade.get()
        }
        cadastrar_paciente(dados)

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except Exception:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
