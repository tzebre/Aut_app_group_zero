import tkinter as tk
import customtkinter as ctk
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
        self.photo_frame = {}
        self.make_frame()
    def info(self):
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size_w = min((4 / 3) * h, w)
        size_h = (3 / 4) * size_w
        self.window_height = int(size_h)
        self.window_width = int(size_w)
        x = 0
        y = 0

        #self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, int(x), int(y)))
        self.geometry("{}x{}+{}+{}".format(w, h, int(x), int(y)))

    def make_frame(self):
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=5, uniform="group1")
        self.grid_rowconfigure(0, weight=1)
        left = tk.Frame(self, bg="red")
        right = tk.Frame(self, bg="blue")
        left.grid(row=0, column=0, sticky="nsew")
        right.grid(row=0, column=1,sticky="nsew")
        color = [["green", "yellow", "orange"],["orange","green", "yellow"]]
        right.grid_rowconfigure(0, weight=10, uniform="group1")
        right.grid_rowconfigure(1, weight=1, uniform="group1")
        right.grid_columnconfigure(0, weight=1, uniform="group1")
        btm = tk.Frame(right, bg="pink")
        btm.grid(row=0, column=0, sticky="nsew")
        self.photo_frame = {0:{}, 1:{}}
        for r in range(2):
            btm.grid_rowconfigure(r, weight=1)
            for c in range(3):
                btm.grid_columnconfigure(c, weight=1, uniform="group1")
                self.photo_frame[r][c] = tk.Frame(btm, bg=color[r][c])
                self.photo_frame[r][c].grid(row=r, column=c, sticky="nsew")

app = Application()
app.mainloop()