# ========================================
# UNIVERSIDADE DE MOGI DAS CRUZES - UMC
# Professor: Luiz Carlos dos Santos Filho
# Programa: Mini-Projeto de Software Básico (versão PostgreSQL)
# Desenvolvido por: Edney Leandro Gonçalves, Gustavo Seiji, João Pedro Duo,
#                   João Pedro Perez e Willi Hasman
# Data: 03/12/2025
# CUSTOMTKINTER
# Bibliotecas
# ========================================

import customtkinter as ctk
from tkinter import ttk
import os
import time
import json
from PIL import Image, ImageTk 
import psycopg2
from psycopg2 import errors
from dotenv import load_dotenv

# ----------------- JANELA PRINCIPAL -----------------
class HEALTHTRACK_APP (ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HEALTH TRACK - O sistema que cuida de você")
        self.geometry("900x600")

        # FRAME LATERAL (MENU)
        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.configure(fg_color="#FFFFFF")

        # Logo no menu
        self.image = Image.open("interface/HEALTH TRACK.png")
        self.image_menu = ctk.CTkImage(
            light_image=self.image,
            dark_image=self.image,
            size=(50, 50) # tamanho desejado
        )
        # Cria o Label com a logo
        logo_label_menu = ctk.CTkLabel(self.menu_frame, image=self.image_menu, text="")
        logo_label_menu.pack(pady=20)

        # Label menu
        self.label_menu = ctk.CTkLabel(
            self.menu_frame, text="MENU",
            text_color="#0B395C", 
            font=("Arial", 18, "bold")
        )
        self.label_menu.pack(pady=20)

        # botão Home
        self.btn_Home = ctk.CTkButton(
            self.menu_frame, text="🏠",
            width=70,
            height=40,
            text_color="#FFFFFF",
            command=self.Tela_Home,
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="white"
        )
        self.btn_Home.configure(fg_color="#0B395C")
        self.btn_Home.pack(pady=10)

        # botão listar pacientes
        self.btn_listar = ctk.CTkButton(
            self.menu_frame, text="Listar Pacientes",
            text_color="#FFFFFF",
            command=self.listar,
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="white",
            font=("Arial", 12, "bold")
        )
        self.btn_listar.configure(fg_color="#0B395C")
        self.btn_listar.pack(pady=10)

        # botão sair
        self.btn_sair = ctk.CTkButton(
            self.menu_frame, text="Sair", fg_color="#d9534f",
            text_color="#FFFFFF",
            hover_color="#c9302c",
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="white",
            font=("Arial", 12, "bold"), 
            command=self.destroy
        )
        self.btn_sair.pack(pady=50)

        # FRAME PRINCIPAL (TELAS)
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.main_frame.configure(fg_color="#AEE1F5")

        self.Tela_Home()

    def Mudar_Home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def Tela_Home(self):
        self.Mudar_Home()

        self.Logo()

        # Titulo na pagina inicial
        titulo = ctk.CTkLabel(
            self.main_frame, text="Bem-Vindo ao Programa HEALTH TRACK!\n"
            "O sistema que cuida de você.",
            text_color="#FFFFFF",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=20)

    def Logo(self):
        # Abre a imagem
        image = Image.open("interface/HEALTH TRACK.png")
        # Redimensiona a imagem
        logo_img = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(200, 200) # tamanho desejado
        )
        # Cria o Label com a logo
        logo_label = ctk.CTkLabel(self.main_frame, image=logo_img, text="")
        logo_label.pack(pady=20)

    def cadastrar(self):
        # Criar subtela
        janela = ctk.CTkToplevel(self)
        janela.title("Cadastro de Paciente")
        janela.geometry("600x500")
        janela.grab_set()  # trava interação com a janela principal até fechar

        titulo = ctk.CTkLabel(janela, text="Cadastro de Pacientes", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)

        nome = ctk.CTkEntry(janela, placeholder_text="Nome Completo")
        nome.pack(pady=10)

        idade = ctk.CTkEntry(janela, placeholder_text="Idade")
        idade.pack(pady=10)

        Cpf = ctk.CTkEntry(janela, placeholder_text="CPF")
        Cpf.pack(pady=10)

        Rg = ctk.CTkEntry(janela, placeholder_text="RG")
        Rg.pack(pady=10)

        genero = ctk.CTkEntry(janela, placeholder_text="Gênero")
        genero.pack(pady=10)

        estado_saude = ctk.CTkEntry(janela, placeholder_text="Estado de saúde")
        estado_saude.pack(pady=10)

        historico_doencas = ctk.CTkEntry(janela, placeholder_text="Histórico de doenças")
        historico_doencas.pack(pady=10)

        salvar = ctk.CTkButton(janela, text="Salvar")
        salvar.pack(pady=20)

    def listar(self):
        self.Mudar_Home()

        self.paciente_selecionado = None

        # Limpa o frame antes de mostrar a nova tabela
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Lista de Pacientes", text_color="#FFFFFF", font=("Arial", 22, "bold")).pack(pady=10)

        lista_frame = ctk.CTkScrollableFrame(self.main_frame, width=600, height=450)
        lista_frame.pack(pady=10)

        try:
            with open("interface/dados.txt", "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    dados = linha.strip().split(",")

                    card = ctk.CTkFrame(lista_frame, corner_radius=12, fg_color="#E8F1FF")  # azul claro
                    card.pack(fill="x", pady=8, padx=10)

                    nome = ctk.CTkLabel(card, text=dados[0], text_color="#0B395C", font=("Arial", 18, "bold"))
                    nome.pack(anchor="w", padx=10, pady=3)

                    info_label = ctk.CTkLabel(card, text=f"Idade: {dados[1]} | CPF: {dados[2]} | RG: {dados[3]}",
                                      text_color="#000000", font=("Arial", 14))
                    info_label.pack(anchor="w", padx=10)

                    info2_label = ctk.CTkLabel(card, text=f"Gênero: {dados[4]} | Saúde: {dados[5]} | Histórico: {dados[6]}",
                                       text_color="#000000", font=("Arial", 14))
                    info2_label.pack(anchor="w", padx=10, pady=3)

                    # efeito hover
                    def on_enter(e, f=card):
                        f.configure(fg_color="#54ACF0")

                    def on_leave(e, f=card):
                        f.configure(fg_color="#E8F1FF")

                    def Button_on(e, f=card):
                        f.configure(fg_color="#54ACF0")

                    # todos os widgets que devem ativar o hove
                    widgets = [card, nome, info_label, info2_label]

                    for w in widgets:
                        w.bind("<Enter>", on_enter)
                        w.bind("<Leave>", on_leave)
                        w.bind("<Button-1>", Button_on)
        except:
            ctk.CTkLabel(self.main_frame, text="Arquivo 'pacientes.txt' não encontrado!").pack()

        # botões do frame
        botoes_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        botoes_frame.pack(pady=10)

        # botão cadastro
        self.btn_cadastro = ctk.CTkButton(
            botoes_frame, text="Cadastrar Paciente",
            text_color="#FFFFFF",
            command=self.cadastrar,
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="black",
            font=("Arial", 12, "bold")
        )
        self.btn_cadastro.configure(fg_color="#0B395C")
        self.btn_cadastro.pack(side="left", pady=10)

        # botão relatórios
        self.btn_relatorios = ctk.CTkButton(
            botoes_frame, text="Gerar Relatório",
            text_color="#FFFFFF",
            command=self.relatorio,
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="black",
            font=("Arial", 12, "bold")
        )
        self.btn_relatorios.configure(fg_color="#0B395C")
        self.btn_relatorios.pack(side="left", pady=10)

    def atualizar(self):
        pass

    def relatorio(self):
        pass

    def conectar(self):
        pass

    def excluir(self):
        pass



app = HEALTHTRACK_APP()
app.mainloop()