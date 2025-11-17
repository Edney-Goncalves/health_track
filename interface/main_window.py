import tkinter as tk
from tkinter import ttk

from interface.screens.home import HomeScreen
from interface.screens.cadastro import CadastroScreen
from interface.screens.lista import ListaScreen
from interface.screens.editar import EditarScreen
from interface.screens.excluir import ExcluirScreen


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Health Track - Sistema de Pacientes")
        self.root.geometry("650x420")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.frames = {}

        telas = {
            "home": HomeScreen,
            "cadastro": CadastroScreen,
            "lista": ListaScreen,
            "editar": EditarScreen,
            "excluir": ExcluirScreen
        }

        for nome, Tela in telas.items():
            frame = Tela(container, self)
            self.frames[nome] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_screen("home")

    def show_screen(self, nome):
        self.frames[nome].tkraise()

    def run(self):
        self.root.mainloop()
