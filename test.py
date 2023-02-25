import tkinter as tk
import customtkinter as ctk
from PIL import Image
import glob
import random

img_path = "img/*.jpg"


def random_img():
    images = glob.glob(random.choice([img_path]))
    random_image = random.choice(images)
    print(random_image)
    return random_image


def get_frame_size(frame):
    frame.update()
    w = frame.winfo_width()
    h = frame.winfo_height()
    return w, h


def convert_photoimg(source, size):
    photo_image = ctk.CTkImage(light_image=Image.open(source), dark_image=Image.open(source),
                               size=(size[0], size[1]))
    return photo_image


class Pastchoice(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.count = 0
        self.all_past = {}

    def add_img(self, source_img, size):
        self.count += 1
        old = ctk.CTkButton(self, fg_color="grey", hover_color="palegreen",
                            command=lambda count=self.count, source=source_img: self.go_past(count, source),
                            image=convert_photoimg(source_img, size), text=self.count,
                            compound="bottom")
        old.pack(side="bottom", pady=(5, 5))
        self.all_past[self.count] = old

    def go_past(self, count, source):
        self.count = count
        print(count)
        for i in range(count + 1, len(self.all_past) + 1):
            print(i)
            self.all_past[i].destroy()
            self.all_past.pop(i)
        # comment relancer un placmement d'image depuis cette classe ?


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
        self.h_past = None
        self.w_past = None
        self.scroll_left = None
        self.window_height = None
        self.window_width = None
        self.size_photo = None
        self.entropy_slider =None
        self.entropy_value = None
        self.title("zero")
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

        # self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, int(x), int(y)))
        self.geometry("{}x{}+{}+{}".format(w, h, int(x), int(y)))

    def make_frame(self):
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=5, uniform="group1")
        self.grid_rowconfigure(0, weight=1)
        right = tk.Frame(self, bg="blue")
        left = tk.Frame(self, bg="red")
        left.grid(row=0, column=0, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(0, weight=1)
        w, h = get_frame_size(left)
        self.w_past = w * 0.8
        self.h_past = self.w_past
        self.scroll_left = Pastchoice(master=left)
        self.scroll_left.grid(sticky="nsew")
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=10, uniform="group1")
        right.grid_rowconfigure(1, weight=1, uniform="group1")
        right.grid_columnconfigure(0, weight=1, uniform="group1")
        top = tk.Frame(right)
        top.grid(row=0, column=0, sticky="nsew")
        btm = tk.Frame(right)
        btm.grid(row=1, column=0, sticky="nsew")
        btm.columnconfigure(0, weight=2, uniform="group1")
        btm.columnconfigure(1, weight=2, uniform="group1")
        btm.columnconfigure(2, weight=1, uniform="group2")
        self.entropy_slider = ctk.CTkSlider(master=btm, from_=0, to=100, command=self.change_value)
        self.entropy_slider.grid(row=0, column=0, sticky="nsew")
        self.entropy_value = ctk.CTkLabel(master = btm, text=f"entropy : {self.entropy_slider.get():.02f}")
        self.entropy_value.grid(row=0, column=1, sticky="nsew")
        end = ctk.CTkButton(btm, text="Validation finale")
        end.grid(row=0, column=2)
        self.photo_frame = {0: {}, 1: {}}
        for r in range(2):
            top.grid_rowconfigure(r, weight=1)
            if r == 0:
                pady = (10, 5)
            else:
                pady = (5, 10)
            for c in range(3):
                if c == 1:
                    padx = (5, 5)
                elif c == 2:
                    padx = (5, 10)
                else:
                    padx = (10, 5)
                top.grid_columnconfigure(c, weight=1, uniform="group1")
                self.photo_frame[r][c] = {
                    'btn': ctk.CTkButton(top, fg_color="grey", hover_color="palegreen",
                                         command=lambda coords=(r, c): self.button_click(coords), text="_"),
                    'clicked': False, 'order': None, 'source': ""}
                self.photo_frame[r][c]['btn'].grid(row=r, column=c, sticky="nsew", padx=padx, pady=pady)
                w, h = get_frame_size(right)
                w = w // 3.5
                h = h // 2.5
                self.size_photo = (w, h)
        self.new_image()
    def change_value(self, val):
        self.entropy_value.configure(text = f"entropy : {val:.02f}")
    def button_click(self, coords):
        r = coords[0]
        c = coords[1]
        focus_btn = self.photo_frame[r][c]
        if focus_btn["clicked"]:
            focus_btn['btn'].configure(fg_color="palegreen")
            focus_btn['clicked'] = False
        else:
            self.unselect_all()
            focus_btn['btn'].configure(fg_color="darkgreen")
            focus_btn['clicked'] = True
            self.scroll_left.add_img(focus_btn['source'], (self.w_past, self.h_past))
            self.new_image()

    def unselect_all(self):
        for r in range(2):
            for c in range(3):
                self.photo_frame[r][c]['btn'].configure(fg_color="grey")
                self.photo_frame[r][c]['clicked'] = False

    def new_image(self):
        for r in range(2):
            for c in range(3):
                source = random_img()
                print(source)
                self.photo_frame[r][c]['source'] = source
                self.photo_frame[r][c]['btn'].configure(image=convert_photoimg(source, self.size_photo),
                                                        compound='top')


app = Application()
app.mainloop()
