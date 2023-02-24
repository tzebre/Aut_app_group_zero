import numpy as np
import torch
import tkinter as tk
import customtkinter as ctk
import math
class Application(ctk.CTk):
    """
    class principale de gestion de l'application
    Creation de la fenetre
    Creation des frame de base
    Creation du menu
    Appel de la classe settings
    """

    def __init__(self):
        super().__init__()
        self.title("")
        self.info()
    def info(self):
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size_w = min((4 / 3) * h, w)
        size_h = (3 / 4) * size_w
        self.window_height = int(size_h)
        self.window_width = int(size_w)
        x = w // 2 - size_w // 2
        y = h // 2 - size_h // 2
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, int(x), int(y)))
app = Application()
app.mainloop()