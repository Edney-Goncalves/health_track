import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from services.pacientes_service import PacienteService

class CadastroScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        self.build_logo()

        tk.Label(self, text="Cadastro de Paciente", font=("Verdana", 12, "bold"),
                 fg="blue", bg="white").place(x=220, y=140)

        # -------- CAMPOS --------

        tk.Label(self, text="Nome", bg="white").place(x=180, y=180)
        self.nome = tk.Entry(self, width=25)
        self.nome.place(x=300, y=180)

        tk.Label(self, text="CPF", bg="white").place(x=180, y=210)
        self.cpf = tk.Entry(self, width=25)
        self.cpf.place(x=300, y=210)

        tk.Label(self, text="RG", bg="white").place(x=180, y=240)
        self.rg = tk.Entry(self, width=25)
        self.rg.place(x=300, y=240)

        tk.Label(self, text="Idade", bg="white").place(x=180, y=270)
        self.idade = tk.Entry(self, width=25)
        self.idade.place(x=300, y=270)

        tk.Label(self, text="Gênero", bg="white").place(x=180, y=300)
        self.genero = ttk.Combobox(self, values=["Masculino", "Feminino", "Outro"], width=22)
        self.genero.place(x=300, y=300)

        tk.Label(self, text="Estado de Saúde", bg="white").place(x=180, y=330)
        self.estado_saude = tk.Entry(self, width=25)
        self.estado_saude.place(x=300, y=330)

        tk.Label(self, text="Histórico de Doenças (JSON)", bg="white").place(x=180, y=360)
        self.historico = tk.Entry(self, width=25)
        self.historico.insert(0, "[]")
        self.historico.place(x=300, y=360)

        # -------- BOTÕES --------

        tk.Button(self, text="Salvar", width=18, command=self.salvar).place(x=240, y=400)
        tk.Button(self, text="Voltar", width=10,
                  command=lambda: controller.show_screen("home")).place(x=10, y=360)

    def salvar(self):
        dados = {
            "name": self.nome.get(),
            "cpf": self.cpf.get(),
            "rg": self.rg.get(),
            "age": self.idade.get(),
            "gender": self.genero.get(),
            "health_state": self.estado_saude.get(),
            "disease_history": self.historico.get()
        }

        try:
            PacienteService.cadastrar(dados)
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
            self.limpar_campos()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos(self):
        self.nome.delete(0, tk.END)
        self.cpf.delete(0, tk.END)
        self.rg.delete(0, tk.END)
        self.idade.delete(0, tk.END)
        self.genero.set("")
        self.estado_saude.delete(0, tk.END)
        self.historico.delete(0, tk.END)
        self.historico.insert(0, "[]")

    def build_logo(self):
        try:
            image = Image.open("HEALTH TRACK.png").convert("RGBA")
            image = image.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo_img, bg="white").place(x=250, y=0)
        except:
            tk.Label(self, text="[LOGO]", bg="white").place(x=270, y=20)
