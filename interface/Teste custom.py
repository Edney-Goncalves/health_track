import customtkinter as ctk

# ----------------- CONFIGURAÇÕES GLOBAIS -----------------
ctk.set_appearance_mode("blue")  # Fundo claro
ctk.set_default_color_theme("blue")  # Azul claro moderno

# ----------------- JANELA PRINCIPAL -----------------
class HealthTrackApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HEALTH TRACK - Sistema Hospitalar")
        self.geometry("900x600")
        self.resizable(False, False)

        # FRAME LATERAL (MENU)
        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")

        self.title_label = ctk.CTkLabel(
            self.menu_frame, text="MENU", 
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=20)

        self.btn_cadastro = ctk.CTkButton(
            self.menu_frame, text="Cadastro de Pacientes",
            command=self.show_cadastro
        )
        self.btn_cadastro.pack(pady=10)

        self.btn_relatorios = ctk.CTkButton(
            self.menu_frame, text="Relatórios",
            command=self.show_relatorios
        )
        self.btn_relatorios.pack(pady=10)

        self.btn_sair = ctk.CTkButton(
            self.menu_frame, text="Sair", fg_color="#d9534f",
            hover_color="#c9302c", command=self.destroy
        )
        self.btn_sair.pack(pady=50)

        # FRAME PRINCIPAL (TELAS)
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Inicializa com a tela de cadastro
        self.show_cadastro()

    # ----------------- TELA CADASTRO -----------------
    def show_cadastro(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.main_frame, text="Cadastro de Pacientes",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        form_frame = ctk.CTkFrame(self.main_frame, width=500, height=400)
        form_frame.pack(pady=10)

        # CAMPOS DO FORMULÁRIO
        labels_entries = [
            ("Nome Completo:", "nome"),
            ("Idade:", "idade"),
            ("CPF:", "cpf"),
            ("Telefone:", "telefone"),
            ("Endereço:", "endereco"),
            ("Sintomas:", "sintomas")
        ]

        self.entries = {}

        for label, key in labels_entries:
            lbl = ctk.CTkLabel(form_frame, text=label, anchor="w")
            lbl.pack(pady=5)
            ent = ctk.CTkEntry(form_frame, width=400, placeholder_text=f"Digite {label.lower()}")
            ent.pack(pady=5)
            self.entries[key] = ent

        salvar_btn = ctk.CTkButton(
            form_frame, text="Salvar Dados",
            fg_color="#1e90ff", hover_color="#1c86ee",
            width=200
        )
        salvar_btn.pack(pady=20)

    # ----------------- TELA RELATÓRIOS -----------------
    def show_relatorios(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.main_frame, text="Relatórios de Pacientes",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        relatorio_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        relatorio_frame.pack(fill="both", expand=True, padx=20, pady=20)

        info = ctk.CTkLabel(
            relatorio_frame,
            text="Aqui futuramente aparecerão os relatórios dos pacientes.\n"
                 "Você poderá buscar, filtrar e exportar informações.",
            font=("Arial", 16),
            justify="center"
        )
        info.pack(pady=40)


# ----------------- EXECUÇÃO -----------------
if __name__ == "__main__":
    app = HealthTrackApp()
    app.mainloop()

def listar(self):
        # Limpa o frame antes de mostrar a nova tabela
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Lista de Pacientes", text_color="#000000", font=("Arial", 22, "bold")).pack(pady=10)

        lista_frame = ctk.CTkScrollableFrame(self.main_frame, width=600, height=450)
        lista_frame.pack(pady=10)

        try:
            with open("interface/dados.txt", "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    dados = linha.strip().split(",")

                    card = ctk.CTkFrame(lista_frame, corner_radius=12, fg_color="#E8F1FF")  # azul claro
                    card.pack(fill="x", pady=8, padx=10)

                    nome = ctk.CTkLabel(card, text=dados[0], font=("Arial", 18, "bold"))
                    nome.pack(anchor="w", padx=10, pady=3)

                    info = f"Idade: {dados[1]} | CPF: {dados[2]} | RG: {dados[3]}"
                    ctk.CTkLabel(card, text=info, font=("Arial", 14)).pack(anchor="w", padx=10)

                    info2 = f"Gênero: {dados[4]} | Saúde: {dados[5]} | Histórico: {dados[6]}"
                    ctk.CTkLabel(card, text=info2, font=("Arial", 14)).pack(anchor="w", padx=10, pady=3)
        except:
            ctk.CTkLabel(self.main_frame, text="Arquivo 'pacientes.txt' não encontrado!").pack()