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
from tkinter import messagebox
import os
import time
import json
import traceback
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
        self.resizable(False, False)

        # FRAME LATERAL (MENU)
        self.menu_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)
        self.menu_frame.configure(fg_color="#FFFFFF")

        # Logo no menu
        self.image = Image.open("interface/HEALTH TRACK.png")
        self.image_menu = ctk.CTkImage(
            light_image=self.image,
            dark_image=self.image,
            size=(60, 60) # tamanho desejado
        )

        # botão Home com a imagem
        self.btn_Home = ctk.CTkButton(
            self.menu_frame,
            image=self.image_menu,
            text="",
            width=80,
            height=50,
            command=self.Tela_Home
        )
        self.btn_Home.configure(hover_color="#F0F0F0")
        self.btn_Home.configure(fg_color="transparent")
        self.btn_Home.pack(pady=10, padx=20)

        # Label menu
        self.label_menu = ctk.CTkLabel(
            self.menu_frame, text="MENU",
            text_color="#0B395C", 
            font=("Arial", 20, "bold")
        )
        self.label_menu.pack(pady=20, padx=20)

        # botão listar pacientes
        self.btn_listar = ctk.CTkButton(
            self.menu_frame, text="Pacientes",
            text_color="#FFFFFF",
            command=self.listar,
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="white",
            hover_color="#54ACF0",
            font=("Arial", 16, "bold")
        )
        self.btn_listar.configure(fg_color="#0B395C")
        self.btn_listar.pack(pady=5, padx=20)

        # Espaçamento antes do ATALHO
        self.espaco_atalho = ctk.CTkLabel(self.menu_frame, text="", height=10)
        self.espaco_atalho.pack()

        # Opções da Lista de pacientes
        self.menu_pacientes = ctk.CTkLabel(
            self.menu_frame, text="ATALHO",
            text_color="#0B395C", 
            font=("Arial", 20, "bold")
        )
        self.menu_pacientes.pack(pady=20, padx=20)

        # botões do frame
        self.botoes_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.botoes_frame.pack()

        # botão cadastro
        self.btn_cadastro = ctk.CTkButton(
            self.botoes_frame, text="Cadastrar Paciente",
            text_color="#FFFFFF",
            command=self.cadastrar,
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="white",
            hover_color="#54ACF0",
            font=("Arial", 16, "bold")
        )
        self.btn_cadastro.configure(fg_color="#0B395C")
        self.btn_cadastro.pack(pady=5, padx=20)

        # botão excluir 
        self.btn_excluir = ctk.CTkButton(
            self.botoes_frame, text="Excluir Paciente",
            text_color="#FFFFFF",
            command=self.excluir,
            hover_color="#c9302c",
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="white",
            font=("Arial", 16, "bold")
        )
        self.btn_excluir.configure(fg_color="#0B395C")
        self.btn_excluir.pack(pady=5, padx=20)

        # botão relatórios
        self.btn_relatorios = ctk.CTkButton(
            self.botoes_frame, text="Gerar Relatório",
            text_color="#FFFFFF",
            command=self.relatorio,
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="white",
            hover_color="#54ACF0",
            font=("Arial", 16, "bold")
        )
        self.btn_relatorios.configure(fg_color="#0B395C")
        self.btn_relatorios.pack(pady=5, padx=20)

        # ESPAÇO FLEXÍVEL para empurrar o botão Sair para baixo
        self.espaco_flexivel = ctk.CTkLabel(self.menu_frame, text="")
        self.espaco_flexivel.pack(fill="y", expand=True, padx=20)

        # botão sair
        self.btn_sair = ctk.CTkButton(
            self.menu_frame, text="Sair", fg_color="#d9534f",
            text_color="#FFFFFF",
            hover_color="#c9302c",
            corner_radius=10,   # arredondado
            border_width=2,
            border_color="white",
            font=("Arial", 16, "bold"), 
            command=self.destroy
        )
        self.btn_sair.pack(pady=20, padx=20)

        # Botão Configurações
        # self.btn_config = ctk.CTkButton(
        #    self.menu_frame
        #)
        #self.btn_config.pack(padx=20)

        # FRAME PRINCIPAL (TELAS)
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.main_frame.configure(fg_color="#AEE1F5")

        # Inicialmente escondidos
        self.esconder_atalhos()

        self.Tela_Home()

    def carregar_pacientes(self):
        # Carrega do novo local
        pacientes = []
        try:
            # Tenta carregar do novo local
            caminho_arquivo = "interface/dados.txt"

            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                    for linha in arquivo:
                        linha = linha.strip()
                        if linha:  
                            dados = linha.split(",")
                            # remove espaços em branco dos campos
                            dados = [dado.strip() for dado in dados]

                            if len(dados) >= 7:  # Verifica se tem todos os campos
                                paciente = {
                                    'nome': dados[0],
                                    'idade': dados[1],
                                    'cpf': dados[2],
                                    'rg': dados[3],
                                    'genero': dados[4],
                                    'saude': dados[5],
                                    'historico': dados[6]
                                }
                                pacientes.append(paciente)
                print(F"Carregados {len(pacientes)} pacientes de: {caminho_arquivo}") # Debug
        except Exception as e:
            print(f"Erro ao carregar pacientes: {e}")
        return pacientes
    
    def salvar_pacientes(self, pacientes):
        # Salva a lista de dicionários no arquivo
        try:
            # Salva na mesma pasta do seu script Python
            caminho_arquivo = "interface/dados.txt"

            print(F"Tentando salvar em: {os.path.abspath(caminho_arquivo)}")

            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                for paciente in pacientes:
                    linha = F"{paciente['nome']}, {paciente['idade']}, {paciente['cpf']}, {paciente['rg']}, {paciente['genero']}, {paciente['saude']}, {paciente['historico']}\n"
                    arquivo.write(linha)

            print(f"Salvos {len(pacientes)} pacientes em: {caminho_arquivo}")
            return True
        
        except Exception as e:
            print(f"Erro detalhado ao salvar: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")
            return False           

    def mostrar_atalhos(self):
        # Mostra os botões de atalho no menu
        try:

            # Remove temporariamente o espaço flexível e o botão sair
            self.espaco_flexivel.pack_forget() 
            self.btn_sair.pack_forget()   

            # Mostra os atalhos na ordem correta
            self.espaco_atalho.pack()
            self.menu_pacientes.pack(pady=10, padx=20)
            self.botoes_frame.pack(pady=10, padx=20, fill="x")

            # recoloca o espaço flexível e o botão sair (agora abaixo dos atalhos)
            self.espaco_flexivel.pack(fill="y", expand=True, padx=20)
            self.btn_sair.pack(pady= 20, padx=20)

        except Exception as e:
            print(f"Erro ao mostrar atalhos: {e}")

    def esconder_atalhos(self):
        # Enconde os botões de atalho no menu
        try:
            self.espaco_atalho.pack_forget()
            self.menu_pacientes.pack_forget()
            self.botoes_frame.pack_forget()
        except Exception as e:
            print(f"Erro ao mostrar atalhos: {e}")

    def Mudar_Home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def Tela_Home(self):
        self.Mudar_Home()

        self.Logo()

        self.esconder_atalhos()

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
        janela.geometry("650x500")
        janela.grab_set()  # trava interação com a janela principal até fechar

        titulo = ctk.CTkLabel(janela, text="Cadastro de Pacientes", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)

        # Frame principal com scroll
        main_scroll_frame = ctk.CTkScrollableFrame(janela)
        main_scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Frame principal para o formulário dentro do scrollable frame
        frame_prin = ctk.CTkFrame(main_scroll_frame)
        frame_prin.pack(pady=20, padx=40, fill="both", expand=True)

        # Configurar grid para organizar os campos
        frame_prin.grid_columnconfigure(0, weight=1)
        frame_prin.grid_columnconfigure(1, weight=1)

        # Linha 1: Nome (ocupa duas colunas)
        ctk.CTkLabel(frame_prin, text="Nome Completo", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 5))
        nome = ctk.CTkEntry(frame_prin, placeholder_text="Digite o nome completo", height=40)
        nome.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")

        # Linha 2: idade e gênero
        ctk.CTkLabel(frame_prin, text="Idade", font=("Arial", 14, "bold")).grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))

        ctk.CTkLabel(frame_prin, text="Gênero", font=("Arial", 14, "bold")).grid(row=2, column=1, sticky="w", padx=20, pady=(10, 5))

        idade = ctk.CTkEntry(frame_prin, placeholder_text="Ex: 25", height=40)
        idade.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")

        genero = ctk.CTkComboBox(frame_prin, values=["Masculino", "Feminino", "Não Binário"], height=40, dropdown_font=("Arial", 12))
        genero.set("Selecione")
        genero.grid(row=3, column=1, padx=20, pady=(0, 15), sticky="ew")

        # Linha 3: CPF e RG
        ctk.CTkLabel(frame_prin, text="CPF", font=("Arial", 14, "bold")).grid(row=4, column=0, sticky="w", padx=20, pady=(10, 5))
        ctk.CTkLabel(frame_prin, text="RG", font=("Arial", 14, "bold")).grid(row=4, column=1, sticky="w", padx=20, pady=(10, 5))

        Cpf = ctk.CTkEntry(frame_prin, placeholder_text="000.000.000-00", height=40)
        Cpf.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="ew")

        Rg = ctk.CTkEntry(frame_prin, placeholder_text="00.000.000-0", height=40)
        Rg.grid(row=5, column=1, padx=20, pady=(0, 15), sticky="ew")

        # Linha 4: Estado de Saúde
        ctk.CTkLabel(frame_prin, text="Estado de Saúde", font=("Arial", 14, "bold")).grid(row=6, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 5))

        estado_saude = ctk.CTkComboBox(frame_prin, values=["Não Urgência", "Urgência", "Emergência"], height=40, dropdown_font=("Arial", 12))
        estado_saude.set("Selecione o estado de saúde")
        estado_saude.grid(row=7, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")

        # Linha 5: Histórico de Doenças
        ctk.CTkLabel(frame_prin, text="Histórico de Doenças", font=("Arial", 14, "bold")).grid(row=8, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 5))

        historico_doencas = ctk.CTkEntry(frame_prin, placeholder_text="Ex: Diabetes, Hipertensão...", height=40)
        historico_doencas.grid(row=9, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        # Frame para os botões
        botoes_frame_prin = ctk.CTkFrame(janela, fg_color="transparent")
        botoes_frame_prin.pack(pady=20)

        # Botões
        salvar = ctk.CTkButton(botoes_frame_prin, text="Salvar Cadastro", font=("Arial", 16, "bold"), height=45, command=lambda: self.salvar_cadastro(nome, idade, Cpf, Rg, genero, estado_saude, historico_doencas, janela))
        salvar.pack(side="left", padx=10)

        cancelar = ctk.CTkButton(botoes_frame_prin, text="Cancelar", font=("Arial", 16, "bold"), height=45,
                                 fg_color="#6c757d", hover_color="#c9302c",
                                  command=janela.destroy)
        cancelar.pack(side="left", padx=10)

        self.configurar_validacoes_tempo_real(nome, idade, Cpf, Rg)

    def validar_cadastro(self, dados):
        # Faz todas as validações dos dados do paciente
        erros = []

        # 1. Validação do Nome
        if not dados['nome'] or dados['nome'].strip() == "":
            erros.append("Nome completo é obrigatório")
        elif len(dados['nome'].strip()) < 3:
            erros.append("Nome deve ter pelo menos 3 caracteres")
        elif any(char.isdigit() for char in dados['nome']):
            erros.append("Nome não pode conter números")

        # 2. Validação da Idade
        if not dados['idade'] or dados['idade'].strip == "":
            erros.append("Idade é obrigatória")
        else:
            try:
                idade_num = int(dados['idade'])
                if idade_num < 0 or idade_num > 150:
                    erros.append("Idade deve estar entre 0 e 150 anos")
            except ValueError:
                erros.append("Idade deve ser um número válido")

        # 3. Validação do CPF
        if not dados['cpf'] or dados['cpf'].strip() == "":
            erros.append("CPF é obrigatório")  
        else:
            cpf_limpo = ''.join(filter(str.isdigit, dados['cpf']))
            if len(cpf_limpo) != 11:
                erros.append("CPF deve ter 11 dígitos")
            # Teste mais complexo:
            #elif not self.validar_cpf(cpf_limpo):
                #erros.append("CPF inválido")

        # 4. Validação do RG
        if not dados['rg'] or dados['rg'].strip() == "":
            erros.append("RG é obrigatório")
        else:
            rg_limpo = ''.join(filter(str.isdigit, dados['rg']))
            if len(rg_limpo) < 9:
                erros.append("RG deve ter pelo menos 9 dígitos")

        # 5. Validação do Gênero
        if not dados['genero'] or dados['genero'] == "Selecione":
            erros.append("Gênero é obrigatório")
        elif dados['genero'] not in ["Masculino", "Feminino", "Não Binário"]:
            erros.append("Gênero deve ser Masculino, Feminino ou Não Binário")

        # 6. Validação do Estado de Saúde
        if not dados['saude'] or dados['saude'] == "Selecione o estado de saúde":
            erros.append("Estado de saúde é obrigatório")
        elif dados['saude'] not in ["Não Urgência", "Urgência", "Emergência"]:
            erros.append("Estado de saúde deve ser: Não Urgência, Urgência, Emergência")

        # 7. Validação do Histórico (Básico)
        if dados['historico'] and len(dados['historico']) > 500:
            erros.append("Histórico muito longo (máximo 500 caracteres)")
        
        return erros
    
    def validar_cpf(self, cpf):
        # Valida o formato do CPF

        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))

        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False

        #Validacao_profissional = {
            # Cálculo do primeiro dígito verificador
            soma = 0
            for i in range(9):
                soma += int(cpf[i]) * (10 - i)
            resto = soma % 11
            digito1 = 0 if resto < 2 else 11 - resto
                
            # Cálculo do segundo dígito verificador
            soma = 0
            for i in range(10):
                soma += int(cpf[i]) * (11 - i)
            resto = soma % 11
            digito2 = 0 if resto < 2 else 11 - resto
                
            # Verifica se os dígitos calculados conferem com os informados
            return int(cpf[9]) == digito1 and int(cpf[10]) == digito2 
        #}

    def formatar_cpf(self, cpf):
        # Formata o CPF para o padrão XXX.XXX.XXX-XX
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        if len(cpf_limpo) == 11:
            return F"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        return cpf
    
    def verificar_cpf_existente(self, cpf):
        # Verifica se o CPF já está cadastrado
        pacientes = self.carregar_pacientes()
        cpf_limpo = ''.join(filter(str.isdigit, cpf))

        for paciente in pacientes:
            paciente_cpf_limpo = ''. join(filter(str.isdigit, paciente['cpf']))
            if paciente_cpf_limpo == cpf_limpo:
                return True
        return False
    
    def verificar_rg_existente(self, rg):
        # Verifica se o CPF já está cadastrado
        pacientes = self.carregar_pacientes()
        rg_limpo = ''.join(filter(str.isdigit, rg))

        for paciente in pacientes:
            paciente_cpf_limpo = ''. join(filter(str.isdigit, paciente['rg']))
            if paciente_cpf_limpo == rg_limpo:
                return True
        return False

    def formatar_rg(self, rg):
        # Formata o RG para o padrão XX.XXX.XXX-X
        rg_limpo = ''.join(filter(str.isdigit, rg))
        if len(rg_limpo) == 9:
            return F"{rg_limpo[:2]}.{rg_limpo[2:5]}.{rg_limpo[5:8]}-{rg_limpo[8:]}"
        return rg

    def salvar_cadastro(self, nome, idade, Cpf, Rg, genero, estado_saude, historico_doencas, janela):
        # Salva o novo paciente no arquivo

        # Coleta de dados
        dados= {
            'nome': nome.get().strip(),
            'idade': idade.get().strip(),
            'cpf': Cpf.get().strip(),
            'rg': Rg.get().strip(),
            'genero': genero.get().strip(),
            'saude': estado_saude.get().strip(),
            'historico': historico_doencas.get().strip()
        }

        # Validações
        erros = self.validar_cadastro(dados)

        if erros:
            mensagem_erro = "Por favor, corrija os seguintes erros:\n\n" + "\n".join(F"{erro}" for erro in erros)
            messagebox.showerror("Erro no Cadastro", mensagem_erro)
            return
        
        # Verifica se o CPF já existe
        if self.verificar_cpf_existente(dados['cpf']):
            messagebox.showerror("Erro", "CPF já cadastrado no sistema!")
            return
        
        # Verifica se o RG já existe
        if self.verificar_rg_existente(dados['rg']):
            messagebox.showerror("Erro", "RG já cadastrado no sistema!")
            return
        
        try:
            # Formata o CPF
            dados['cpf'] = self.formatar_cpf(dados['cpf'])

            # Formata o RG
            dados['rg'] = self.formatar_rg(dados['rg'])

            # Carrega pacientes existentes
            pacientes = self.carregar_pacientes()
                
            # Adiciona novo paciente
            pacientes.append(dados)

            # Salva no arquivo
            if self.salvar_pacientes(pacientes):
                messagebox.showinfo("Sucesso", F"Paciente {dados['nome']} cadastrado com sucesso!")
                janela.destroy()
                self.listar()  # Atualiza a lista
            else:
                messagebox.showerror("Erro", "Erro ao salvar o paciente!")

        except Exception as e:
            messagebox.showerror("Erro", F"Erro ao cadastrar: {str(e)}")

    def configurar_validacoes_tempo_real(self, nome, idade, cpf, rg):
        # Configura validações em tempo real nos campos

        def validar_nome(event):
            texto = nome.get()
            if any(char.isdigit() for char in texto):
                nome.configure(border_color="red")
            else:
                nome.configure(border_color="green")

        def validar_idade(event):
            texto = idade.get()
            try:
                if texto and (int(texto) < 0 or int(texto) > 150):
                    idade.configure(border_color="red")
                else:
                    idade.configure(border_color="green")
            except:
                if texto:
                    idade.configure(border_color="red")

        def validar_cpf_digitacao(event):
            texto = cpf.get()
            cpf_limpo = ''.join(filter(str.isdigit, texto))
            if len(cpf_limpo) == 11:
                cpf.configure(border_color="green")
            else:
                cpf.configure(border_color="orange")

        def validar_rg_digitacao(event):
            texto = rg.get()
            rg_limpo = ''.join(filter(str.isdigit, texto))
            if len(rg_limpo) == 9:
                rg.configure(border_color="green")
            else:
                rg.configure(border_color="orange")

        # Conectar as validações
        nome.bind("<KeyRelease>", validar_nome)
        idade.bind("<KeyRelease>", validar_idade)
        cpf.bind("<KeyRelease>", validar_cpf_digitacao)
        rg.bind("<KeyRelease>", validar_rg_digitacao)

    def listar(self):
        self.mostrar_atalhos()

        self.Mudar_Home()

        self.paciente_selecionado = None

        # Limpa o frame antes de mostrar a nova tabela
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Lista de Pacientes", text_color="#FFFFFF", font=("Arial", 30, "bold")).pack(pady=10)

        lista_frame = ctk.CTkScrollableFrame(self.main_frame, width=610, height=500)
        lista_frame.pack(pady=10)

        # Variável para armazenar o card atualmente selecionado
        self.card_selecionado = None
        self.cards = [] # Lista para armazenar todos os cards

        try:
            # Carrega o dicionário de pacientes
            pacientes = self.carregar_pacientes()

            if not pacientes:
                ctk.CTkLabel(self.main_frame, text="Nenhum paciente cadastrado!", 
                font=("Arial", 16)).pack(pady=20)
                return

            for i, paciente in enumerate(pacientes):
                card = ctk.CTkFrame(lista_frame, corner_radius=12, fg_color="#E8F1FF")  # azul claro
                card.pack(fill="x", pady=8, padx=10)
                self.cards.append(card)

                nome = ctk.CTkLabel(card, text=paciente['nome'], text_color="#0B395C", font=("Arial", 18, "bold"))
                nome.pack(anchor="w", padx=10, pady=3)

                info_label = ctk.CTkLabel(card, text=f"Idade: {paciente['idade']} | CPF: {paciente['cpf']} | RG: {paciente['rg']}",
                text_color="#000000", font=("Arial", 14))
                info_label.pack(anchor="w", padx=10)

                info2_label = ctk.CTkLabel(card, text=f"Gênero: {paciente['genero']} | Saúde: {paciente['saude']} | Histórico: {paciente['historico']}",
                text_color="#000000", font=("Arial", 14))
                info2_label.pack(anchor="w", padx=10, pady=3)

                # Conectar eventos (agora passa o dicionário completo)
                selecionar_func = lambda event, idx=i, card_ref=card, pac=paciente: self.selecionar_paciente(idx, card_ref, pac)

                # Usar lambda para capturar o self correto
                def criar_selecionar(indice, card_ref, pac):
                    return lambda event: self.selecionar_paciente(indice, card_ref, pac)
                
                # Conectar eventos
                selecionar_func = criar_selecionar(i, card, paciente)

                # Ou de forma mais direta:
                selecionar_func = lambda event, idx=i, card_ref=card, pac=paciente: self.selecionar_paciente(idx, card_ref, pac)

                # efeito hover normal
                def on_enter(e, f=card):
                    if f != self.card_selecionado: # Só aplica houver se não estiver selecionado
                        f.configure(fg_color="#54ACF0")

                def on_leave(e, f=card):
                    if f != self.card_selecionado: # Só volta a cor normal se não estiver selecionado
                        f.configure(fg_color="#E8F1FF")

                # todos os widgets que devem ativar o hover e seleção
                widgets = [card, nome, info_label, info2_label]

                for w in widgets:
                    w.bind("<Enter>", on_enter)
                    w.bind("<Leave>", on_leave)
                    w.bind("<Button-1>", selecionar_func) # Agora chama a função de seleção

        except Exception as e:
            ctk.CTkLabel(self.main_frame, text=f"Erro ao carregar pacientes: {str(e)}").pack()

    def selecionar_paciente(self, indice, card, paciente=None):
        # Método para selecionar um paciente e destacar o card

        # Restaura a cor de todos os cards para o padrão
        for i in self.cards:
            i.configure(fg_color="#E8F1FF")

        # Destaca o card selecionado
        card.configure(fg_color="#54ACF0") # Cor de seleção permanente

        # Atualiza o card selecionado atual
        self.card_selecionado = card

        # Se recebemos o paciente como parâmetro (nova estrutura)
        if paciente is not None:
            self.paciente_selecionado = paciente
            print(f"Paciente selecionado: {self.paciente_selecionado['nome']} - CPF: {self.paciente_selecionado['cpf']}")

    def atualizar(self):
        pass

    def relatorio(self):
        # Verifica se há um paciente selecionado
        if not self.paciente_selecionado:
            messagebox.showwarning("Seleção Necessária", "Por favor, selecione um paciente na lista para gerar o relatório")
            return

        # Criar subtela
        self.janela_relatorio = ctk.CTkToplevel(self)
        self.janela_relatorio.title("Relatório do Paciente")
        self.janela_relatorio.geometry("800x650")
        self.janela_relatorio.grab_set()  # trava interação com a janela principal até fechar

        titulo = ctk.CTkLabel(self.janela_relatorio, text="Relatório do Paciente", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)

        # Botões de controle no topo
        botoes_controle_frame = ctk.CTkFrame(self.janela_relatorio, fg_color="transparent")
        botoes_controle_frame.pack(pady=10, padx=20, fill="x")

        # Botões de confirmação (inicialmente escondidos)
        self.botoes_confirmacao_frame = ctk.CTkFrame(botoes_controle_frame, fg_color="transparent")

        btn_controle_salvar = ctk.CTkButton(self.botoes_confirmacao_frame, text="Salvar", font=("Arial", 14, "bold"),
                                            height=40, fg_color="#0B395C", hover_color="#54ACF0", command=self.salvar_edicao_rapida)
        btn_controle_salvar.pack(side="left", padx=5)

        btn_controle_cancelar = ctk.CTkButton(self.botoes_confirmacao_frame, text="Cancelar", font=("Arial", 14, "bold"),
                                              height=40, fg_color="#6c757d", hover_color="#c9302c", command=self.desativar_modo_edicao)
        btn_controle_cancelar.pack(side="left", padx=5)

         # Espaço flexível
        ctk.CTkLabel(botoes_controle_frame, text="", width=0).pack(side="left", fill="x", expand=True)

        # Frame principal com scroll
        self.main_scroll_frame = ctk.CTkScrollableFrame(self.janela_relatorio, fg_color="white")
        self.main_scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Variáveis para armazenar os widgets editáveis
        self.widgets_edicao = {}
        self.dados_originais = self.paciente_selecionado.copy()

        # Frame do cabeçalho com foto e informações básicas
        header_frame = ctk.CTkFrame(self.main_scroll_frame, fg_color="#E8F1FF")
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)

        # Ícone/Foto do paciente (lado esquerdo)
        try:
            # Tenta carregar uma imagem padrão ou do paciente
            self.foto_paciente = Image.open("interface/avatar.jpg")  # Carrega a imagem

            self.foto_menu = ctk.CTkImage(
                light_image=self.foto_paciente,
                dark_image=self.foto_paciente,
                size=(120, 120)
            )
            foto_label = ctk.CTkLabel(header_frame, image=self.foto_menu, text="")
            foto_label.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nsew")
        except:
            # Se não encontrar imagem, usa um label com ícone textual
            foto_placeholder = ctk.CTkLabel(header_frame, text="👤", font=("Arial", 48), width=120, height=120, fg_color="#0B395C", corner_radius=60)
            foto_placeholder.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nsew")

        # Cabeçalho editável
        # Nome (editável) informações principais (lado direito)
        ctk.CTkLabel(header_frame, text="Nome:", font=("Arial", 12, "bold"), text_color="#54ACF0").grid(row=0, column=1, sticky="w", pady=(20, 0))
        self.widgets_edicao['nome'] = ctk.CTkLabel(header_frame, 
                                              text=self.paciente_selecionado['nome'],
                                              font=("Arial", 24, "bold"),
                                              text_color="#0B395C")
        self.widgets_edicao['nome'].grid(row=1, column=1, sticky="w", pady=(0, 5))

        # Idade e Gênero (editáveis)
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.grid(row=2, column=1, sticky="w", pady=5)

        ctk.CTkLabel(info_frame, text="Idade:", font=("Arial", 12, "bold"), text_color="#54ACF0").pack(side="left")
        self.widgets_edicao['idade'] = ctk.CTkLabel(info_frame, 
                                               text=f"{self.paciente_selecionado['idade']} anos",
                                               font=("Arial", 16), text_color="#000000")
        self.widgets_edicao['idade'].pack(side="left", padx=(5, 20))

        ctk.CTkLabel(info_frame, text="Gênero:", font=("Arial", 12, "bold"), text_color="#54ACF0").pack(side="left")
        self.widgets_edicao['genero'] = ctk.CTkLabel(info_frame, 
                                                text=self.paciente_selecionado['genero'],
                                                font=("Arial", 16),
                                                text_color="#000000")
        self.widgets_edicao['genero'].pack(side="left", padx=5)

        # Estado de Saúde (editável)
        ctk.CTkLabel(header_frame, text="Estado de Saúde:", font=("Arial", 12, "bold"), text_color="#54ACF0").grid(row=3, column=1, sticky="w", pady=(5, 20))
        self.widgets_edicao['saude'] = ctk.CTkLabel(header_frame, 
                                               text=self.paciente_selecionado['saude'],
                                               font=("Arial", 14, "bold"),
                                               text_color=self.cor_estado_saude(self.paciente_selecionado['saude']))
        self.widgets_edicao['saude'].grid(row=4, column=1, sticky="w", pady=(0, 20))

        # Frame de informações pessoais editáveis
        info_frame = ctk.CTkFrame(self.main_scroll_frame, fg_color="white")
        info_frame.pack(fill="x", padx=10, pady=10)

        # Título das informações
        ctk.CTkLabel(info_frame, text="Informações Pessoais", font=("Arial", 18, "bold"),
                     text_color="#0B395C").pack(anchor="w", padx=20, pady=(15, 10))
        
        # Grid para informações em duas colunas
        info_frame_inner = ctk.CTkFrame(info_frame, fg_color="white")
        info_frame_inner.pack(fill="x", padx=20, pady=10)
        info_frame_inner.grid_columnconfigure(0, weight=1)
        info_frame_inner.grid_columnconfigure(1, weight=1)

        # Coluna 1 - CPF e RG (editáveis)
        self.criar_info_item_editavel(info_frame_inner, "CPF:", "cpf", self.paciente_selecionado['cpf'], 0, 0)
        self.criar_info_item_editavel(info_frame_inner, "RG:", "rg", self.paciente_selecionado['rg'], 1, 0)

        # Coluna 2 - Estado de Saúde (somente para demonstração)
        self.criar_info_item_editavel(info_frame_inner, "Estado de Saúde:", "saude", self.paciente_selecionado['saude'], 0, 1)

        # Frame do histórico médico (editável)
        historico_frame = ctk.CTkFrame(self.main_scroll_frame, fg_color="white")
        historico_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(historico_frame, text="Histórico Médico",
                     font=("Arial", 18, "bold"),
                    text_color="#0B395C").pack(anchor="w", padx=20, pady=(15, 10))
        
        self.widgets_edicao['historico'] = ctk.CTkTextbox(historico_frame, height=120, font=("Arial", 14), wrap="word")
        self.widgets_edicao['historico'].pack(fill="x", padx=20, pady=(0, 15))
        self.widgets_edicao['historico'].insert("1.0", self.paciente_selecionado['historico'] or "Nenhum histórico registrado")
        self.widgets_edicao['historico'].configure(state="disabled") # Somente leitura

        # Frame de observações 
        observacoes_frame = ctk.CTkFrame(self.main_scroll_frame, fg_color="white")
        observacoes_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(observacoes_frame, text="Observações", font=("Arial", 18, "bold"),
                     text_color="#0B395C").pack(anchor="w", padx=20, pady=(15, 10))
        
        # Botão editar (lado direito)
        self.btn_editar_obs = ctk.CTkButton(observacoes_frame, text="Editar", font=("Arial", 12, "bold"),
                                            width=80, height=30, fg_color="#0B395C", hover_color="#54ACF0",
                                            command=lambda: self.ativar_edicao_obs())
        self.btn_editar_obs.pack(side="right")

        # Botões salvar e cancelar (inicialmente escondidos)
        self.botoes_edicao_frame = ctk.CTkFrame(observacoes_frame, fg_color="transparent")
        # Inicialmente escondidos
        self.botoes_edicao_frame.pack_forget()

        btn_salvar_obs = ctk.CTkButton(self.botoes_edicao_frame, text="Salvar", font=("Arial", 12, "bold"),
                                       width=80, height=30, fg_color="#0B395C", hover_color="#54ACF0",
                                       command=lambda: self.salvar_obs())
        btn_salvar_obs.pack(side="left", padx=2)

        btn_cancelar_obs = ctk.CTkButton(self.botoes_edicao_frame, text="Cancelar", font=("Arial", 12, "bold"),
                                        width=80, height=30, fg_color="#6c757d", hover_color="#c9302c",
                                        command=lambda: self.cancelar_edicao_obs())
        btn_cancelar_obs.pack(side="left", padx=2)

        # Label explicativo
        ctk.CTkLabel(observacoes_frame, 
                     text="Adicione observações adicionais...",
                     font=("Arial", 12), text_color="#000000").pack(anchor="w", padx=20, pady=(0, 5))
        
        # Área de texto das observações
        self.observacoes_text = ctk.CTkTextbox(observacoes_frame, height=80, font=("Arial", 14),
                                          wrap="word")
        self.observacoes_text.pack(fill="x", padx=20, pady=(0, 15))

        # Carrega as observações atuais (se houver)
        obs_atuais = self.paciente_selecionado.get('observacoes', '')
        self.observacoes_text.insert("1.0", obs_atuais or "Nenhuma observação registrada")
        self.observacoes_text.configure(state="disabled") # inicialmente somente leitura

        # Variável para armazenar texto original (para cancelamento)
        self.obs_original = obs_atuais

        # Inicialmente em mode de leitura
        self.modo_edicao_ativo = False

        # Botões de ação
        botoes_frame = ctk.CTkFrame(self.janela_relatorio, fg_color="transparent")
        botoes_frame.pack(pady=15, padx=20, anchor="center")

        # Botão editar (lado esquerdo)
        self.btn_modo_edicao = ctk.CTkButton(botoes_controle_frame, text="Editar", font=("Arial", 14, "bold"),
                                   height=40, fg_color="#0B395C", hover_color="#54ACF0", command= self.ativar_modo_edicao)
        self.btn_modo_edicao.pack(side="left", padx=5)

        # Botão fechar (centralizado)
        btn_fechar = ctk.CTkButton(botoes_frame, text="Fechar", font=("Arial", 14, "bold"),
                                   height=40, fg_color="#6c757d", command=self.janela_relatorio.destroy, hover_color="#c9302c")
        btn_fechar.pack(side="left", padx=5)

        # Botão excluir (lado direito)
        btn_excluir = ctk.CTkButton(botoes_frame, text="Excluir", font=("Arial", 14, "bold"),
                                   height=40, fg_color="#0B395C", hover_color="#c9302c", command=lambda: self.excluir_paciente_relatorio(self.janela_relatorio))
        btn_excluir.pack(side="right", padx=5)

    # Método auxiliar para criar itens de informação
    def criar_info_item_editavel(self, parent, label, campo, valor, row, column):
        # Cria um item de informação que pode ser editado
        frame_item = ctk.CTkFrame(parent, fg_color="transparent")
        frame_item.grid(row=row, column=column, sticky="ew", padx=10, pady=5)
    
        ctk.CTkLabel(frame_item, text=label, font=("Arial", 14, "bold"),
                 text_color="#555555").pack(anchor="w")
    
        self.widgets_edicao[campo] = ctk.CTkLabel(frame_item, 
                                             text=valor or "Não informado", 
                                             font=("Arial", 14),
                                             text_color="#000000")
        self.widgets_edicao[campo].pack(anchor="w")

    def ativar_modo_edicao(self):
        # Ativa o modo de edição para todos os campos

        if self.modo_edicao_ativo:
            return
    
        self.modo_edicao_ativo = True
        
        # Interface - esconde/mostra botões
        self.btn_modo_edicao.pack_forget()
        self.botoes_confirmacao_frame.pack(side="left", padx=5)
        
        # 1. Histórico médico 
        if 'historico' in self.widgets_edicao:
            self.widgets_edicao['historico'].configure(state="normal")
            print("Histórico habilitado")


        # 2. Habilita observações
        self.ativar_edicao_obs()
        print("Observações habilitadas")

        # 3. Campos Básicos
        self.criar_campos_edicao_simples()

        messagebox.showinfo("Edição Ativada",
                            "Mode de edição ativado!")
        
    def criar_campos_edicao_simples(self):
        # Cria uma janela simples para editar campos básicos
        try:
            # Janela de edição rápida
            janela_edicao = ctk.CTkToplevel(self.janela_relatorio)
            janela_edicao.title("Edição de Dados")
            janela_edicao.geometry("400X500")
            janela_edicao.grab_set()

            titulo = ctk.CTkLabel(janela_edicao, text="Editar Dados do Paciente", font=("Arial", 18, "bold"))
            titulo.pack(pady=20)

            # Frame com scroll
            scroll_frame = ctk.CTkScrollableFrame(janela_edicao)
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

            # Dicionário para armazenar os campos
            self.campos_edicao_rapida = {}

            # 1. Nome
            ctk.CTkLabel(scroll_frame, text="Nome:", 
                        font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
            nome_entry = ctk.CTkEntry(scroll_frame, font=("Arial", 14), height=40)
            nome_entry.insert(0, self.paciente_selecionado['nome'])
            nome_entry.pack(fill="x", pady=(0, 10))
            self.campos_edicao_rapida['nome'] = nome_entry
            
            # 2. Idade
            ctk.CTkLabel(scroll_frame, text="Idade:", 
                        font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
            idade_entry = ctk.CTkEntry(scroll_frame, font=("Arial", 14), height=40)
            idade_entry.insert(0, self.paciente_selecionado['idade'])
            idade_entry.pack(fill="x", pady=(0, 10))
            self.campos_edicao_rapida['idade'] = idade_entry
            
            # 3. Gênero
            ctk.CTkLabel(scroll_frame, text="Gênero:", 
                        font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
            genero_entry = ctk.CTkComboBox(scroll_frame, values=["Masculino", "Feminino", "Não Binário"], dropdown_font=("Arial", 14), height=40)
            genero_entry.set("Selecione")
            genero_entry.grid(fill="x", pady=(0, 10))
            self.campos_edicao_rapida['genero'] = genero_entry
            
            # 4. CPF
            ctk.CTkLabel(scroll_frame, text="CPF:", 
                        font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
            cpf_entry = ctk.CTkEntry(scroll_frame, font=("Arial", 14), height=40)
            cpf_entry.insert(0, self.paciente_selecionado['cpf'])
            cpf_entry.pack(fill="x", pady=(0, 10))
            self.campos_edicao_rapida['cpf'] = cpf_entry
            
            # 5. RG
            ctk.CTkLabel(scroll_frame, text="RG:", 
                        font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
            rg_entry = ctk.CTkEntry(scroll_frame, font=("Arial", 14), height=40)
            rg_entry.insert(0, self.paciente_selecionado['rg'])
            rg_entry.pack(fill="x", pady=(0, 10))
            self.campos_edicao_rapida['rg'] = rg_entry
            
            # 6. Estado de Saúde
            ctk.CTkLabel(scroll_frame, text="Estado de Saúde:", 
                        font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
            saude_entry = ctk.CTkEntry(scroll_frame, font=("Arial", 14), height=40)
            saude_entry.insert(0, self.paciente_selecionado['saude'])
            saude_entry.pack(fill="x", pady=(0, 10))
            self.campos_edicao_rapida['saude'] = saude_entry

            # Botões
            botoes_frame = ctk.CTkFrame(janela_edicao, fg_color="transparent")
            botoes_frame.pack(pady=20)

            btn_salvar = ctk.CTkButton(botoes_frame, text="Salvar", command=lambda: self.salvar_edicao_rapida(janela_edicao))
            btn_salvar.pack(side="left", padx=10)

            btn_cancelar = ctk.CTkButton(botoes_frame, text="Cancelar", command=janela_edicao.destroy)
            btn_cancelar.pack(side="left", padx=10)

            print("Janela de edição criada")
        except Exception as e:
            print(F"Erro ao criar janela de edição: {e}")
            traceback.print_exc()

    def salvar_edicao_rapida(self, janela_edicao):
        # Salva as edições da janela rápida
        try:
            dados_editados = self.dados_originais.copy()

            # Coleta dados dos campos
            for campo, entry in self.campos_edicao_rapida.items():
                dados_editados[campo] = entry.get().strip()

            # Validações
            erros = self.validar_cadastro(dados_editados)
            if erros:
                mensagem_erro = "Erros encontrados:\n\n" + "\n".join(F"• {erro}" for erro in erros)
                messagebox.showerror("Erro na Edição", mensagem_erro)
                return
            
            # Salva no arquivo
            pacientes = self.carregar_pacientes()
            for i, paciente in enumerate(pacientes):
                if paciente['cpf'] == self.dados_originais['cpf']:
                    pacientes[i] = dados_editados
                    break

            if self.salvar_pacientes(pacientes):
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                self.paciente_selecionado = dados_editados
                janela_edicao.destroy()
                self.janela_relatorio.destroy()
                self.listar()
            else:
                messagebox.showerror("Erro", "Erro ao salvar dados!")

        except Exception as e:
            messagebox.showerror("Erro", F"Erro ao salvar: {str(e)}")

    def desativar_modo_edicao(self):
        # Desativa o modo de edição
        if not self.modo_edicao_ativo:
            return
        
        self.modo_edicao_ativo = False
        
        # Mostra botão Editar, esconde botões Salvar/Cancelar
        self.botoes_confirmacao_frame.pack_forget()
        self.btn_modo_edicao.pack(side="left", padx=5)

        # Desabilita apenas os campos que habilitamos
        if 'historico' in self.widgets_edicao:
            self.widgets_edicao['historico'].configure(state="disabled")
        
        # Desabilita observações
        self.desativar_edicao_obs()

        print("Modo de edição desativado")
        
    # Método para definir cores baseadas no estado de saúde
    def cor_estado_saude(self, estado):
        # Retorna a cor baseada no estado de saúde
        cores = {
            "Não Urgência": "#28a745", # verde
            "Urgência": "#ffc107", # amarelo
            "Emergência": "#dc3545" # vermelho
        }
        return cores.get(estado, "#666666")
    
    # Método para editar paciente (placeholder)
    def editar_paciente(self, janela):
        # Abre a tela de edição do paciente
        messagebox.showinfo("Editar", F"Editando paciente: {self.paciente_selecionado['nome']}")
        janela.destroy()

    def excluir_paciente_relatorio(self):
        pass

    def ativar_edicao_obs(self):
        # Ativa o modo de edição das observações

        # Esconde botão editar
        self.btn_editar_obs.pack_forget()

        # Mostra botões Salvar/Cancelar
        self.botoes_edicao_frame.pack(side="right")

        # Habilita a edição do texto
        self.observacoes_text.configure(state="normal")
        self.observacoes_text.focus()

        # Se for o texto padrão, limpa para edição
        if self.observacoes_text.get("1.0", "end-1c") == "Nenhuma observação registrada":
            self.observacoes_text.delete("1.0", "end")

    def desativar_edicao_obs(self):
        # Desativa o modo de edição das observações

        # Esconde botões Salvar/Cancelar
        self.botoes_edicao_frame.pack_forget()

        # Mostra botão editar
        self.btn_editar_obs.pack(side="right")

        # Desabilita a edição do texto
        self.observacoes_text.configure(state="disabled")

    def salvar_obs(self):
        # Salva as observações editadas
        try:
            novas_obs = self.observacoes_text.get("1.0", "end-1c").strip()

            # Carrega todos os pacientes
            pacientes = self.carregar_pacientes()

            # Atualiza as observações do paciente selecionado
            for paciente in pacientes:
                if paciente['cpf'] == self.paciente_selecionado['cpf']:
                    paciente['observacoes'] = novas_obs
                    break

            # Salva no arquivo
            if self.salvar_pacientes(pacientes):
                messagebox.showinfo("Sucesso", "Observações salvas com sucesso!")
                # Atualiza o paciente selecionado em memória
                self.paciente_selecionado['observacoes'] = novas_obs
                self.obs_original = novas_obs
            else:
                messagebox.showerror("Erro", "Erro ao salvar observações!")

            # Desativa modo edição
            self.desativar_edicao_obs()

        except Exception as e:
            messagebox.showerror("Erro", F"Erro ao salvar: {str(e)}")

    def cancelar_edicao_obs(self):
        # Cancela a edição e restaura o texto original

        # Restaura o texto original
        self.observacoes_text.configure(state="normal")
        self.observacoes_text.delete("1.0", "end")

        if self.obs_original:
            self.observacoes_text.insert("1.0", self.obs_original)
        else:
            self.observacoes_text.insert("1.0", "Nenhuma observação registrada")

        # Desativa modo edição
        self.desativar_edicao_obs()

    def conectar(self):
        pass

    def excluir(self):
        # Verifica se há um paciente selecionado
        if not self.paciente_selecionado:
            messagebox.showwarning("Seleção Necessária", "Por favor, selecione um paciente na lista para excluir!")
            return
        
        # Verificar o que está no paciente_selecionado
        print(F"Tentando excluir: {self.paciente_selecionado}")
        
        # Confirmação antes de excluir
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            F"Tem certeza que deseja excluir permanentemente o paciente?\n\n"
            F"Nome: {self.paciente_selecionado['nome']}\n"
            F"CPF: {self.paciente_selecionado['cpf']}\n\n"
            F"Esta ação não pode ser desfeita!"
        )

        if not resposta:
            return # Usuário cancelou a exclusão

        try:
            # Carrega todos os pacientes
            pacientes = self.carregar_pacientes()
            print(f"Total de pacientes antes: {len(pacientes)}")

            # Mostrar todos os Cpfs
            for i, p in enumerate(pacientes):
                print(F"Paciente {i}: {p['nome']} - CPF: {p['cpf']}")

            # Filtra removendo o paciente selecionado
            pacientes_atualizados = []   
            paciente_encontrado = False

            for paciente in pacientes:
                # Comparar CPFs (remover possiveis espaços)
                cpf_arquivo = paciente['cpf'].strip()
                cpf_selecionado = self.paciente_selecionado['cpf'].strip()

                if cpf_arquivo != cpf_selecionado:
                    pacientes_atualizados.append(paciente)
                else:
                    paciente_encontrado = True
                    print(f"Paciente encontrado e será removido: {paciente['nome']}")
            
            print(f"Paciente encontrado: {paciente_encontrado}")
            print(f"Total de pacientes depois: {len(pacientes_atualizados)}")

            # Verifica se realmente removeu alguém
            if not paciente_encontrado:
                messagebox.showerror("Erro", 
                    f"Paciente não encontrado no arquivo!\n"
                    f"Procurando CPF: {self.paciente_selecionado['cpf']}")
                return
            
            # Salva a lista atualizada
            self.salvar_pacientes(pacientes_atualizados)
            # Mensagem de sucesso
            messagebox.showinfo(
                "Exclusão Concluida",
                F"Paciente {self.paciente_selecionado['nome']} foi excluído com sucesso!"
            )

            # Atualiza a interface
            self.paciente_selecionado = None
            self.card_selecionado = None
            self.listar()  # Atualiza a lista visual

        except Exception as e:
            messagebox.showerror("Erro", F"Erro ao excluir: \n{str(e)}")
            print(F"Erro detalhado: {e}")



app = HEALTHTRACK_APP()
app.mainloop()