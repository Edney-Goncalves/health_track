import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.pacientes_service import excluir_paciente


class ExcluirScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(style="Main.TFrame")

        # Título
        titulo = ttk.Label(
            self,
            text="Excluir Paciente",
            style="Titulo.TLabel"
        )
        titulo.pack(pady=20)

        # Campo de ID
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(
            form_frame,
            text="ID do Paciente:",
            style="Label.TLabel"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.id_entry = ttk.Entry(form_frame, width=25)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Botão Excluir
        excluir_btn = ttk.Button(
            self,
            text="Excluir",
            style="Primary.TButton",
            command=self.excluir_paciente
        )
        excluir_btn.pack(pady=20)

        # Botão Voltar
        voltar_btn = ttk.Button(
            self,
            text="Voltar",
            style="Secondary.TButton",
            command=lambda: controller.show_screen("home")
        )
        voltar_btn.pack(pady=5)

    def excluir_paciente(self):
        paciente_id = self.id_entry.get().strip()

        if not paciente_id:
            tk.messagebox.showerror("Erro", "Digite o ID do paciente.")
            return

        sucesso = excluir_paciente(paciente_id)

        if sucesso:
            tk.messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
            self.id_entry.delete(0, tk.END)
        else:
            tk.messagebox.showerror("Erro", "Pacient não encontrado.")
