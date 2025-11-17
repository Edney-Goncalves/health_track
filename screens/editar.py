import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.pacientes_service import PacienteService


class EditarScreen(tk.Frame): 
    def __init__(self, parent, controller):
        print("Carregou HOME")
        super().__init__(parent, bg="white") 
        self.controller = controller
        self.build_logo()

        tk.Label(
            self,
            text="Atualizar Paciente",
            font=("Verdana", 12, "bold"),
            fg="blue",
            bg="white"
        ).place(x=220, y=140)

        # CPF
        tk.Label(self, text="CPF do paciente", bg="white").place(x=180, y=190)
        self.cpf = tk.Entry(self, width=25)
        self.cpf.place(x=300, y=190)

        # Novo nome
        tk.Label(self, text="Novo Nome", bg="white").place(x=180, y=230)
        self.nome = tk.Entry(self, width=25)
        self.nome.place(x=300, y=230)

        # Botão salvar
        tk.Button(self, text="Salvar Alterações", width=18,
                  command=self.salvar).place(x=240, y=300)

        tk.Button(self, text="Voltar", width=10,
                  command=lambda: controller.show_screen("home")).place(x=10, y=360)

    def salvar(self):
        PacienteService.atualizar(
            self.cpf.get(),
            "name",
            self.nome.get()
        )

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
