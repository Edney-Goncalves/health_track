import tkinter as tk
from PIL import Image, ImageTk

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.build_logo()

        tk.Label(self, text="Menu Principal", font=("Verdana", 14, "bold"),
                 fg="blue", bg="white").place(x=230, y=150)

        tk.Button(self, text="Cadastrar Paciente", width=25,
                  command=lambda: controller.show_screen("cadastro")).place(x=200, y=200)

        tk.Button(self, text="Listar Pacientes", width=25,
                  command=lambda: controller.show_screen("lista")).place(x=200, y=240)

        tk.Button(self, text="Editar Paciente", width=25,
                  command=lambda: controller.show_screen("editar")).place(x=200, y=280)

        tk.Button(self, text="Excluir Paciente", width=25,
                  command=lambda: controller.show_screen("excluir")).place(x=200, y=320)

        #tk.Button(self, text="Gerar Relatório", width=25,
         #         command=lambda: controller.show_screen("relatorio")).place(x=200, y=360)

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=240, y=10)
        except:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
