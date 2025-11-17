import tkinter as tk

# IMPORTA AS TELAS
from screens.home import HomeScreen
from screens.cadastro import CadastroScreen
from screens.lista import ListaScreen
from screens.editar import EditarScreen
from screens.excluir import ExcluirScreen



class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HealthTrack")
        self.geometry("600x500")
        self.resizable(False, False)

        # container central onde as telas ficarão empilhadas
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}  # dicionário -> guarda instâncias das telas

        # todas as telas que existirão
        telas = {
            "home": HomeScreen,
            "cadastro": CadastroScreen,
            "lista": ListaScreen,
            "editar": EditarScreen,
            "excluir": ExcluirScreen,
        }

        # cria cada tela UMA VEZ e guarda em self.frames
        for nome, TelaClass in telas.items():
            frame = TelaClass(container, self)
            self.frames[nome] = frame
            frame.place(relwidth=1, relheight=1)

        # mostra a tela inicial
        self.show_screen("home")

    def show_screen(self, nome_tela):
        """Traz a tela desejada para frente sem recriar nada."""
        frame = self.frames[nome_tela]
        frame.tkraise()

