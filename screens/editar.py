import customtkinter as ctk
from tkinter import messagebox
from core.repository import PacienteRepository

class EditarScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#AEE1F5")

        titulo = ctk.CTkLabel(self, text="Editar Paciente", text_color="#0B395C", font=("Arial",18,"bold"))
        titulo.pack(pady=12)

        self.form = ctk.CTkFrame(self, fg_color="white")
        self.form.pack(padx=18, pady=8, fill="x")

        self.nome = ctk.CTkEntry(self.form, placeholder_text="Nome completo", height=36)
        self.nome.pack(fill="x", padx=12, pady=(12,6))
        self.idade = ctk.CTkEntry(self.form, placeholder_text="Idade", height=36)
        self.idade.pack(fill="x", padx=12, pady=6)
        self.cpf = ctk.CTkEntry(self.form, placeholder_text="CPF (não editável)", height=36, state="disabled")
        self.cpf.pack(fill="x", padx=12, pady=6)
        self.rg = ctk.CTkEntry(self.form, placeholder_text="RG", height=36)
        self.rg.pack(fill="x", padx=12, pady=6)
        self.genero = ctk.CTkComboBox(self.form, values=["Masculino","Feminino","Não Binário"])
        self.genero.pack(fill="x", padx=12, pady=6)
        self.saude = ctk.CTkComboBox(self.form, values=["Não Urgência","Urgência","Emergência"])
        self.saude.pack(fill="x", padx=12, pady=6)
        self.historico = ctk.CTkTextbox(self.form, height=100, wrap="word")
        self.historico.pack(fill="both", padx=12, pady=(6,12))

        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.pack(pady=10)
        btn_salvar = ctk.CTkButton(botoes, text="Salvar Alterações", command=self.salvar, width=160, height=40)
        btn_salvar.pack(side="left", padx=8)
        btn_cancel = ctk.CTkButton(botoes, text="Cancelar", fg_color="#6c757d", hover_color="#c9302c", command=lambda: controller.show_screen("lista"))
        btn_cancel.pack(side="left", padx=8)

    def on_show(self):
        # popula campos com paciente selecionado
        p = self.controller.selected_patient
        if not p:
            messagebox.showwarning("Nenhum paciente", "Selecione um paciente na lista antes de editar.")
            self.controller.show_screen("lista")
            return

        self.nome.delete(0,"end"); self.nome.insert(0, p.get("name",""))
        self.idade.delete(0,"end"); self.idade.insert(0, str(p.get("age","")))
        self.cpf.configure(state="normal"); self.cpf.delete(0,"end"); self.cpf.insert(0, p.get("cpf","")); self.cpf.configure(state="disabled")
        self.rg.delete(0,"end"); self.rg.insert(0, p.get("rg",""))
        self.genero.set(p.get("gender","Selecione"))
        self.saude.set(p.get("health_state","Selecione o estado de saúde"))
        # disease_history pode ser JSON/array
        hist = p.get("disease_history")
        if isinstance(hist, (list, tuple)):
            texto = "\n".join([str(x) for x in hist])
        else:
            texto = str(hist) if hist else ""
        self.historico.delete("1.0","end"); self.historico.insert("1.0", texto)

    def salvar(self):
        p = self.controller.selected_patient
        if not p:
            messagebox.showerror("Erro", "Nenhum paciente selecionado.")
            return

        dados_edit = {
            "name": self.nome.get().strip(),
            "age": self.idade.get().strip(),
            "cpf": p["cpf"],  # chave inalterável
            "rg": self.rg.get().strip(),
            "gender": self.genero.get(),
            "health_state": self.saude.get(),
            "disease_history": [self.historico.get("1.0","end-1c").strip()]
        }

        # validações mínimas
        erros = []
        if not dados_edit["name"] or len(dados_edit["name"]) < 3:
            erros.append("Nome inválido")
        try:
            ai = int(dados_edit["age"])
            if ai < 0 or ai > 150:
                erros.append("Idade inválida")
        except:
            erros.append("Idade inválida")

        if erros:
            messagebox.showerror("Erros", "\n".join(erros))
            return

        try:
            # atualiza campo por campo
            PacienteRepository.atualizar(dados_edit["cpf"], "name", dados_edit["name"])
            PacienteRepository.atualizar(dados_edit["cpf"], "age", int(dados_edit["age"]))
            PacienteRepository.atualizar(dados_edit["cpf"], "rg", dados_edit["rg"])
            PacienteRepository.atualizar(dados_edit["cpf"], "gender", dados_edit["gender"])
            PacienteRepository.atualizar(dados_edit["cpf"], "health_state", dados_edit["health_state"])
            PacienteRepository.atualizar(dados_edit["cpf"], "disease_history", dados_edit["disease_history"])

            messagebox.showinfo("Sucesso", "Dados atualizados")
            # atualiza seleção em memória
            self.controller.selected_patient = PacienteRepository.buscar_por_cpf(dados_edit["cpf"])
            self.controller.show_screen("lista")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar:\n{e}")
