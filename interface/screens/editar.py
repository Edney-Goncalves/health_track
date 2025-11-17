import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.pacientes_service import atualizar_paciente


class EditarScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="white")
        self.build_logo()

        # Título
        tk.Label(
            self,
            text="Atualizar Paciente",
            font=("Verdana", 12, "bold"),
            fg="blue",
            bg="white"
        ).place(x=220, y=140)

        # Campo ID
        tk.Label(self, text="ID", bg="white").place(x=180, y=190)
        self.pid = tk.Entry(self, width=25)
        self.pid.place(x=260, y=190)

        # Campo Nome
        tk.Label(self, text="Novo Nome", bg="white").place(x=180, y=220)
        self.nome = tk.Entry(self, width=25)
        self.nome.place(x=260, y=220)

        # Botão salvar
        tk.Button(
            self,
            text="Salvar Alterações",
            width=18,
            command=self.salvar
        ).place(x=240, y=300)

        # Botão voltar
        tk.Button(
            self,
            text="Voltar",
            width=10,
            command=lambda: controller.show_screen("home")
        ).place(x=10, y=360)

    def salvar(self):
        atualizar_paciente(
            self.pid.get(),
            {"name": self.nome.get()}
        )

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except Exception:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
