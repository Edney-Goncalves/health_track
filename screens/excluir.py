import customtkinter as ctk
from tkinter import messagebox
from core.repository import PacienteRepository

class ExcluirScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#AEE1F5")

        titulo = ctk.CTkLabel(self, text="Excluir Paciente", text_color="#0B395C", font=("Arial",18,"bold"))
        titulo.pack(pady=12)

        info = ctk.CTkLabel(self, text="Selecione um paciente na tela de lista e depois venha aqui para confirmar a exclusão.", font=("Arial",12))
        info.pack(pady=8)

        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.pack(pady=12)
        btn_confirm = ctk.CTkButton(botoes, text="Confirmar Exclusão", fg_color="#d9534f", hover_color="#c9302c", command=self.confirmar, width=180, height=40)
        btn_confirm.pack(side="left", padx=8)
        btn_cancel = ctk.CTkButton(botoes, text="Cancelar", command=lambda: controller.show_screen("lista"))
        btn_cancel.pack(side="left", padx=8)

    def on_show(self):
        p = self.controller.selected_patient
        if not p:
            messagebox.showwarning("Nenhum paciente", "Selecione um paciente na lista antes de excluir.")
            self.controller.show_screen("lista")

    def confirmar(self):
        p = self.controller.selected_patient
        if not p:
            messagebox.showerror("Erro", "Nenhum paciente selecionado.")
            return

        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir:\n\n{p['name']} (CPF: {p['cpf']})")
        if not resposta:
            return

        try:
            PacienteRepository.excluir(p["cpf"])
            messagebox.showinfo("Sucesso", f"Paciente {p['name']} excluído")
            self.controller.selected_patient = None
            self.controller.show_screen("lista")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir:\n{e}")
