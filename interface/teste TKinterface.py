# ========================================
# UNIVERSIDADE DE MOGI DAS CRUZES - UMC
# Professor: Luiz Carlos dos Santos Filho
# Programa: Mini-Projeto de Software Básico (versão PostgreSQL)
# Desenvolvido por: Edney Leandro Gonçalves, Gustavo Seiji, João Pedro Duo,
#                   João Pedro Perez e Willi Hasman
# Data: 03/12/2025
# TKINTER
# Bibliotecas
# ========================================

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from func import cadastrar, listar, atualizar, excluir, relatorio

# Função para Logotipo
def Logo ():
    # Cor de fundo da janela (em RGB)
    bg_color = (255, 255, 255, 255)  # branco com alpha 100%
    # Abre a imagem original com canal alfa (transparência)
    image = Image.open("HEALTH TRACK.png").convert("RGBA")
    # Cria uma nova imagem com o fundo igual ao da janela
    bg_image = Image.new("RGBA", image.size, bg_color)
    image = Image.alpha_composite(bg_image, image)
    # Redimensiona a imagem
    resize_image = image.resize((120, 120))
    # Converte para formato Tkinter
    img = ImageTk.PhotoImage(resize_image)
    # Cria um label com a imagem
    logo_label = Label(Screen, image=img, bg="#FFFFFF", borderwidth=0)
    logo_label.image = img  # mantém referência
    logo_label.place(x=250, y=0)

# Função cadastramento de paciente
def Cadastrar_paciente ():
    cadastrar(Screen)

# Função listar os pacientes
def Listar_paciente ():
    listar(Screen)

# Função atualiza a ficha do paciente
def Atualizar_paciente ():
    atualizar(Screen)

# Função excluir cadastro do paciente
def Excluir_paciente ():
    excluir(Screen)

# Função relatório de pesquisa
def Relatorio_pesquisa ():
    relatorio(Screen)

# Instancia a classe TK e Mostra Container
Screen = Tk()
Screen.configure(bg="#FFFFFF")
Screen.title("HEALTH TRACK - O sistema que cuida de você")
Screen.geometry('620x400') # Dimensiona a janela
# Título do Aplicativo - Widgets Label
Tit = Label(Screen, text="Selecione uma das opções abaixo")
Tit.place(x=190,y=130) # posiona o widgets no container
Tit["font"] = ("Verdana", "10", "italic", "bold",)
Tit["fg"]=("blue")
Tit["bg"]=("white")
# Botão Cadastrar Paciente
BT_Cadastro = Button(Screen, text="Cadastrar Paciente",width=18)
BT_Cadastro.place(x=240,y=180)
BT_Cadastro['command'] = Cadastrar_paciente
# Botão Listar Paciente
BT_Listar = Button(Screen, text="Listar Paciente",width=18)
BT_Listar.place(x=240,y=220)
BT_Listar['command'] = Listar_paciente
# Botão Atualizar Paciente
BT_Listar = Button(Screen, text="Atualizar Paciente",width=18)
BT_Listar.place(x=240,y=260)
BT_Listar['command'] = Atualizar_paciente
# Botão Excluir Paciente
BT_Listar = Button(Screen, text="Excluir Paciente",width=18)
BT_Listar.place(x=240,y=300)
BT_Listar['command'] = Excluir_paciente
# Botão Relatório de pesquisa
BT_Listar = Button(Screen, text="Relatório de pesquisa",width=18)
BT_Listar.place(x=240,y=340)
BT_Listar['command'] = Relatorio_pesquisa
# Botão Sair
Sair= Button(Screen, text="Finalizar o Sistema", command=Screen.destroy,width=15)
Sair.place(x=480,y=360)
# Carrega a Logo
Logo()
# Exibe a Tela
Screen.mainloop()

