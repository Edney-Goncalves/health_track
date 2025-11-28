import customtkinter as ctk
from tkinter import ttk
from core.repository import PacienteRepository


class RelatorioScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.repo = PacienteRepository()

        self.title = ctk.CTkLabel(
            self,
            text="Relatório de Pacientes",
            text_color="#FFFFFF",
            font=("Arial", 22, "bold")
        )
        self.title.pack(pady=20)

        self.table_frame = ctk.CTkFrame(self, fg_color="#E8F1FF")
        self.table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("nome", "idade", "cpf", "rg", "genero", "saude"),
            show="headings",
            height=15
        )

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11))

        self.tree.heading("nome", text="Nome")
        self.tree.heading("idade", text="Idade")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("rg", text="RG")
        self.tree.heading("genero", text="Gênero")
        self.tree.heading("saude", text="Estado de Saúde")

        self.tree.column("nome", width=150)
        self.tree.column("idade", width=60)
        self.tree.column("cpf", width=120)
        self.tree.column("rg", width=120)
        self.tree.column("genero", width=100)
        self.tree.column("saude", width=150)

        self.tree.pack(fill="both", expand=True, pady=10)

        self.btn_exportar = ctk.CTkButton(
            self,
            text="Exportar Relatório (TXT)",
            fg_color="#0B395C",
            text_color="#FFFFFF",
            border_width=2,
            border_color="black",
            corner_radius=10,
            font=("Arial", 12, "bold"),
            command=self.exportar_relatorio
        )
        self.btn_exportar.pack(pady=12)

    def on_show(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        pacientes = self.repo.listar()

        for p in pacientes:
            self.tree.insert(
                "",
                "end",
                values=(
                    p["name"],
                    p["age"],
                    p["cpf"],
                    p.get("rg", "—"),
                    p.get("gender", "—"),
                    p.get("health_state", "—")
                )
            )

    def exportar_relatorio(self):
        pacientes = self.repo.listar()

        with open("relatorio_pacientes.txt", "w", encoding="utf-8") as f:
            f.write("RELATÓRIO DE PACIENTES\n\n")
            for p in pacientes:
                f.write(f"Nome: {p['name']}\n")
                f.write(f"Idade: {p['age']}\n")
                f.write(f"CPF: {p['cpf']}\n")
                f.write(f"RG: {p.get('rg', '—')}\n")
                f.write(f"Gênero: {p.get('gender', '—')}\n")
                f.write(f"Saúde: {p.get('health_state', '—')}\n")
                f.write("-" * 40 + "\n")
