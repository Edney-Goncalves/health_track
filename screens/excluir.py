import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.pacientes_service import PacienteService
from tkinter import messagebox


class ExcluirScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.build_logo()

        tk.Label(self, text="Excluir Paciente", font=("Verdana", 12, "bold"),
                 fg="blue", bg="white").place(x=230, y=140)

        tk.Label(self, text="CPF", bg="white").place(x=180, y=190)
        self.cpf = tk.Entry(self, width=25)
        self.cpf.place(x=260, y=190)

        tk.Button(self, text="Excluir", width=18,
                  command=self.excluir).place(x=240, y=260)
        tk.Button(self, text="Voltar", width=10,
                  command=lambda: controller.show_screen("home")).place(x=10, y=360)

    def excluir(self):
        PacienteService.excluir(self.cpf.get())

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
