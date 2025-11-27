import customtkinter as ctk
from tkinter import messagebox
from core.repository import PacienteRepository

class ListaScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#AEE1F5")
        self.cards = []
        self.card_selected = None

        header = ctk.CTkLabel(self, text="Lista de Pacientes", text_color="#FFFFFF", font=("Arial",20,"bold"))
        header.pack(pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=700, height=480)
        self.scroll_frame.pack(pady=6, padx=12, fill="both", expand=True)

    def on_show(self):
        self.refresh_list()

    def refresh_list(self):
        # limpa
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.cards = []
        self.card_selected = None
        self.controller.selected_patient = None

        try:
            pacientes = PacienteRepository.listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar pacientes:\n{e}")
            return

        if not pacientes:
            ctk.CTkLabel(self.scroll_frame, text="Nenhum paciente cadastrado!", font=("Arial",14)).pack(pady=20)
            return

        for i, p in enumerate(pacientes):
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=12, fg_color="#E8F1FF")
            card.pack(fill="x", pady=8, padx=8)
            self.cards.append(card)

            nome = ctk.CTkLabel(card, text=p["name"], text_color="#0B395C", font=("Arial",16,"bold"))
            nome.pack(anchor="w", padx=10, pady=(8,2))

            info = ctk.CTkLabel(card, text=f"Idade: {p['age']} | CPF: {p['cpf']} | RG: {p['rg']}", text_color="#000000", font=("Arial",12))
            info.pack(anchor="w", padx=10, pady=(0,6))

            info2 = ctk.CTkLabel(card, text=f"Gênero: {p['gender']} | Saúde: {p['health_state']}", text_color="#000000", font=("Arial",12))
            info2.pack(anchor="w", padx=10, pady=(0,10))

            # binds
            def on_enter(e, f=card):
                if f != self.card_selected:
                    f.configure(fg_color="#54ACF0")
            def on_leave(e, f=card):
                if f != self.card_selected:
                    f.configure(fg_color="#E8F1FF")
            def on_click(e, pac=p, f=card):
                self.select_card(pac, f)

            for w in (card, nome, info, info2):
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)
                w.bind("<Button-1>", on_click)

    def select_card(self, paciente, card_widget):
        # restaura todos
        for c in self.cards:
            c.configure(fg_color="#E8F1FF")
        card_widget.configure(fg_color="#54ACF0")
        self.card_selected = card_widget
        self.controller.selected_patient = paciente
        print(f"Selecionado: {paciente['name']} - CPF {paciente['cpf']}")
