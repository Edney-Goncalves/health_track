import customtkinter as ctk
from tkinter import messagebox
from core.repository import PacienteRepository

class CadastroScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#AEE1F5")

        titulo = ctk.CTkLabel(self, text="Cadastro de Pacientes", text_color="#0B395C", font=("Arial",18,"bold"))
        titulo.pack(pady=12)

        form = ctk.CTkFrame(self, fg_color="white")
        form.pack(padx=18, pady=8, fill="x")

        # campos
        self.nome = ctk.CTkEntry(form, placeholder_text="Nome completo", height=36)
        self.nome.pack(fill="x", padx=12, pady=(12,6))

        self.idade = ctk.CTkEntry(form, placeholder_text="Idade", height=36)
        self.idade.pack(fill="x", padx=12, pady=6)

        self.cpf = ctk.CTkEntry(form, placeholder_text="CPF (somente números)", height=36)
        self.cpf.pack(fill="x", padx=12, pady=6)

        self.rg = ctk.CTkEntry(form, placeholder_text="RG", height=36)
        self.rg.pack(fill="x", padx=12, pady=6)

        self.genero = ctk.CTkComboBox(form, values=["Masculino","Feminino","Não Binário"])
        self.genero.set("Selecione")
        self.genero.pack(fill="x", padx=12, pady=6)

        self.saude = ctk.CTkComboBox(form, values=["Não Urgência","Urgência","Emergência"])
        self.saude.set("Selecione o estado de saúde")
        self.saude.pack(fill="x", padx=12, pady=6)

        self.historico = ctk.CTkTextbox(form, height=100, wrap="word")
        self.historico.pack(fill="both", padx=12, pady=(6,12))

        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.pack(pady=10)
        btn_salvar = ctk.CTkButton(botoes, text="Salvar Cadastro", command=self.salvar, width=160, height=40)
        btn_salvar.pack(side="left", padx=8)
        btn_cancel = ctk.CTkButton(botoes, text="Cancelar", fg_color="#6c757d", hover_color="#c9302c", command=lambda: controller.show_screen("home"))
        btn_cancel.pack(side="left", padx=8)

    def validar(self, dados):
        erros = []
        if not dados.get("name") or len(dados["name"].strip()) < 3:
            erros.append("Nome inválido")
        try:
            idade = int(dados.get("age",""))
            if idade < 0 or idade > 150:
                erros.append("Idade inválida")
        except Exception:
            erros.append("Idade inválida")
        cpf = ''.join(filter(str.isdigit, dados.get("cpf","")))
        if len(cpf) != 11:
            erros.append("CPF deve ter 11 dígitos")
        if dados.get("gender") not in ["Masculino","Feminino","Não Binário"]:
            erros.append("Gênero inválido")
        if dados.get("health_state") not in ["Não Urgência","Urgência","Emergência"]:
            erros.append("Estado de saúde inválido")
        return erros

    def salvar(self):
        dados = {
            "name": self.nome.get().strip(),
            "age": self.idade.get().strip(),
            "cpf": ''.join(filter(str.isdigit, self.cpf.get())),
            "rg": self.rg.get().strip(),
            "gender": self.genero.get(),
            "health_state": self.saude.get(),
            # armazenamos histórico como lista com um único texto (repository trata como json)
            "disease_history": [self.historico.get("1.0","end-1c").strip()] 
        }

        erros = self.validar(dados)
        if erros:
            messagebox.showerror("Erros no formulário", "\n".join(erros))
            return

        try:
            # verifica cpf existente
            existing = PacienteRepository.buscar_por_cpf(dados["cpf"])
            if existing:
                messagebox.showerror("Erro", "CPF já cadastrado")
                return

            PacienteRepository.inserir(dados)
            messagebox.showinfo("Sucesso", f"Paciente {dados['name']} cadastrado")
            # limpa campos
            self.nome.delete(0, "end")
            self.idade.delete(0, "end")
            self.cpf.delete(0, "end")
            self.rg.delete(0, "end")
            self.genero.set("Selecione")
            self.saude.set("Selecione o estado de saúde")
            self.historico.delete("1.0", "end")

            # retorna para lista atualizada
            self.controller.show_screen("lista")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar:\n{e}")
