import customtkinter as ctk
from PIL import Image
import tkinter as tk

# telas
from screens.home import HomeScreen
from screens.lista import ListaScreen
from screens.cadastro import CadastroScreen
from screens.editar import EditarScreen
from screens.excluir import ExcluirScreen
from screens.relatorio import RelatorioScreen

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HealthTrack")
        self.geometry("1000x650")
        self.resizable(False, False)

        # estado compartilhado
        self.selected_patient = None

        # layout: menu lateral + area principal
        self.menu_frame = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)
        self.menu_frame.configure(fg_color="#FFFFFF")

        # logo
        try:
            img = Image.open("HEALTH TRACK.png")
            logo = ctk.CTkImage(light_image=img, dark_image=img, size=(60, 60))
            btn_logo = ctk.CTkButton(
                self.menu_frame,
                image=logo,
                text="",
                width=80,
                height=50,
                fg_color="transparent"
            )
            btn_logo.pack(pady=12)
        except Exception:
            ctk.CTkLabel(self.menu_frame, text="HEALTH TRACK", font=("Arial", 16, "bold")).pack(pady=12)

        ctk.CTkLabel(
            self.menu_frame,
            text="MENU",
            text_color="#0B395C",
            font=("Arial", 18, "bold")
        ).pack(pady=(6, 16))

        # botões do menu
        self.btn_home = ctk.CTkButton(
            self.menu_frame,
            text="Home",
            command=lambda: self.show_screen("home")
        )
        self.btn_home.pack(pady=6, padx=20, fill="x")

        self.btn_lista = ctk.CTkButton(
            self.menu_frame,
            text="Pacientes",
            command=lambda: self.show_screen("lista")
        )
        self.btn_lista.pack(pady=6, padx=20, fill="x")

        # atalhos
        ctk.CTkLabel(
            self.menu_frame,
            text="ATALHOS",
            text_color="#0B395C",
            font=("Arial", 14, "bold")
        ).pack(pady=(20, 6))

        self.btn_cadastrar = ctk.CTkButton(
            self.menu_frame,
            text="Cadastrar Paciente",
            command=lambda: self.show_screen("cadastro")
        )
        self.btn_cadastrar.pack(pady=6, padx=20, fill="x")

        self.btn_editar = ctk.CTkButton(
            self.menu_frame,
            text="Editar Paciente",
            command=lambda: self.show_screen("editar")
        )
        self.btn_editar.pack(pady=6, padx=20, fill="x")

        self.btn_excluir = ctk.CTkButton(
            self.menu_frame,
            text="Excluir Paciente",
            command=lambda: self.show_screen("excluir")
        )
        self.btn_excluir.pack(pady=6, padx=20, fill="x")

        # NOVO: botão de relatório
        self.btn_relatorio = ctk.CTkButton(
            self.menu_frame,
            text="Relatório",
            command=lambda: self.show_screen("relatorio")
        )
        self.btn_relatorio.pack(pady=6, padx=20, fill="x")

        # espaçamento flexível
        self.esp = ctk.CTkLabel(self.menu_frame, text="")
        self.esp.pack(expand=True, fill="y")

        self.btn_sair = ctk.CTkButton(
            self.menu_frame,
            text="Sair",
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self.destroy
        )
        self.btn_sair.pack(pady=12, padx=20, fill="x")

        # area principal onde as telas ficarão
        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(side="right", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # registro de telas
        self.frames = {}
        telas = {
            "home": HomeScreen,
            "lista": ListaScreen,
            "cadastro": CadastroScreen,
            "editar": EditarScreen,
            "excluir": ExcluirScreen,
            "relatorio": RelatorioScreen,
        }

        for nome, TelaClass in telas.items():
            frame = TelaClass(self.container, self)
            self.frames[nome] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # mostra inicial
        self.show_screen("home")

    def show_screen(self, nome):
        frame = self.frames.get(nome)
        if not frame:
            return

        # chamada de hook para refresh quando existir
        if hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception as e:
                print("Erro em on_show:", e)

        frame.tkraise()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
