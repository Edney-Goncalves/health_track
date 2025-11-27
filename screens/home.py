import customtkinter as ctk
from PIL import Image
import tkinter as tk

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#AEE1F5")

        # logo grande
        try:
            img = Image.open("HEALTH TRACK.png")
            logo = ctk.CTkImage(light_image=img, dark_image=img, size=(200,200))
            lbl = ctk.CTkLabel(self, image=logo, text="")
            lbl.image = logo
            lbl.pack(pady=30)
        except Exception:
            pass

        titulo = ctk.CTkLabel(self, text="Bem-Vindo ao Programa HEALTH TRACK!\nO sistema que cuida de você.", text_color="#FFFFFF", font=("Arial",18,"bold"))
        titulo.pack(pady=10)
