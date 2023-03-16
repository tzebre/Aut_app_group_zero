import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk
import glob
from itertools import count, cycle
import shutil
import random
import os
from PIL import Image
import AE_GEN as ae
import numpy as np

# TODO choix plusieur images
# TODO Generation et save image


img_path = "dataset/00000/"
last_path = ".past/"
muted_path = ".img/"
past_temp = ".past_temp/"
dir_cache  = ".cache/"
fun = True

H = 64
W = 64
C = 3

def make_thumbnail(list_img):
    print(list_img)
    if len(list_img) > 4:
        row = 3
        col = 2
    elif len(list_img) >1 :
        row = 2
        col = 2
    else :
        row = 1
        col = 1
    dst = Image.new('RGB', (W*col, H*row))
    opened = []
    for i in list_img:
       opened.append(Image.open(i).resize((H, W)))
    for i, im in enumerate(opened):
        if i <2:
            dst.paste(im, (i*W, 0))
        elif i ==2:
            dst.paste(im, (0, H))
        elif i == 3:
            dst.paste(im, (W, H))
        elif i == 4:
            dst.paste(im, (0, 2*H))
        else:
            dst.paste(im, (W, H*2))
    dst.save(f"{dir_cache}thumbnailed.png")
    return f"{dir_cache}thumbnailed.png"

def init_photo_frame():
    for r in range(Application.row):
        Application.photo_frame[r] = {}
        for c in range(Application.col):
            Application.photo_frame[r][c] = None


def change_temp(files):
    for d in os.listdir(past_temp):
        os.remove(f"{past_temp}{d}")
    for f in files:
        shutil.copyfile(f, f"{past_temp}/{f.split('/')[-1]}")


def random_img():
    """
        Retourne une image aléatoire parmi une liste d'images.

        Returns:
            str: Chemin d'accès vers l'image aléatoire sélectionnée.
        """
    images = glob.glob(random.choice([img_path + "*.png"]))
    random_image = random.choice(images)
    return random_image


def created_img():
    files = os.listdir(muted_path)
    for i, f in enumerate(files):
        files[i] = f"{muted_path}{f}"
    files.append(files[-1])
    arr_img = np.array(files)
    img_lst = arr_img.reshape(2, 3)
    return img_lst


def get_frame_size(frame):
    """
    Récupère la taille d'un cadre.

    Args:
        frame (Tkinter.Frame): Cadre dont la taille doit être récupérée.

    Returns:
        tuple: Largeur et hauteur du cadre.
    """
    frame.update()
    w = frame.winfo_width()
    h = frame.winfo_height()
    return w, h


def convert_photoimg(source, size):
    """
        Convertit une image source en un objet Tkinter.PhotoImage.

        Args:
            source (str): Chemin d'accès vers l'image source à convertir.
            size (tuple): Largeur et hauteur de l'image redimensionnée.

        Returns:
            tkinter.PhotoImage: Objet PhotoImage de l'image convertie et redimensionnée.
        """
    if size is None:
        photo_image = ctk.CTkImage(light_image=Image.open(source), dark_image=Image.open(source))
    else:
        photo_image = ctk.CTkImage(light_image=Image.open(source), dark_image=Image.open(source),
                                   size=(size[0], size[1]))
    return photo_image


class Pastchoice(ctk.CTkScrollableFrame):
    # TODO past_temp et past a faire avec les bon path par geenration et afficher image multiple sur scroll
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.count = 0
        self.all_past = {}

    def add_img(self, size):
        """
            Ajoute une image à l'interface graphique sous forme de bouton avec un texte et un compteur.

            Args:
                size (tuple): Largeur et hauteur de l'image redimensionnée.

            Returns:
                None
        """
        self.count += 1
        new_dir = f"{last_path}{self.count}/"
        os.mkdir(new_dir)
        print(Application.selected_source)
        for source_img in list(Application.selected_source["source"].values()):
            end_path = source_img.split("/")[1]
            new_path = new_dir + end_path
            shutil.copyfile(source_img, new_path)
            shutil.copyfile(source_img, f"{past_temp}{end_path}")
        old = ctk.CTkButton(self, fg_color="grey", hover_color="palegreen",
                            command=lambda cnt=self.count, source= Application.selected_source["source"]: self.go_past(cnt),
                            image=convert_photoimg(Application.selected_source["thumbnail"], size), text=self.count,
                            compound="bottom")
        old.pack(side="bottom", pady=(5, 5))
        self.all_past[self.count] = [old, new_dir]

    def go_past(self, cnt):
        """
            Efface tous les boutons d'images qui se trouvent après le bouton sélectionné.

            Args:
                cnt (int): Numéro du bouton sélectionné.

            Returns:
                None
        """
        self.count = cnt
        for i in range(self.count + 1, len(self.all_past) + 1):
            self.all_past[i][0].destroy()
            path = self.all_past[i][1]
            if os.path.exists(path):
                shutil.rmtree(path)
            self.all_past.pop(i)
        files = []
        for f in os.listdir(f"{last_path}{self.count}"):
            files.append(f"{last_path}{self.count}/{f}")
        change_temp(files)
        Application.selected_source["source"] = files
        Application.new_image()


class Application(ctk.CTk):
    photo_frame = {}
    size_photo = None
    selected_source = {"thumbnail":str, "source":{}}
    never = True
    col = 3
    row = 2

    def __init__(self):
        super().__init__()
        self.delay = None
        init_photo_frame()
        self.toplevel = None
        self.end_btn = None
        self.h_past = None
        self.w_past = None
        self.scroll_left = None
        self.entropy_slider = None
        self.entropy_value = None
        self.gif_frame = None
        self.frames = None
        self.title("zero")
        self.info()
        # self.accueil()
        self.make_frame()

    def info(self):
        """
            Détermine les dimensions de la fenêtre en fonction des dimensions de l'écran et positionne la fenêtre en
            haut à gauche de l'écran.

            Args:

            Returns:
                None
            """
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = 0
        y = 0
        self.geometry("{}x{}+{}+{}".format(w, h, int(x), int(y)))

    # def accueil(self):
    #     btm = tk.Frame()
    #     im = Image.open('./file/logo.png')
    #     logo = ImageTk.PhotoImage(im, master=btm)
    #
    #     ##----- Création du canevas et affichage de l'image -----##
    #     dessin = tk.Canvas(btm, width=im.size[0], height=im.size[1])
    #     logo1 = dessin.create_image(0, 0, anchor=tk.NW, image=logo)
    #     dessin.grid()
    #     lan = ctk.CTkButton(btm, text='Lancer', command=self.make_frame)
    #     lan.pack(side=ctk.BOTTOM)

    def make_frame(self):
        """
            Configure et crée les frames nécessaires pour l'interface graphique de l'application.

            Cette méthode configure les colonnes et les rangées de la frame principale, puis crée deux sous-frames :
            une frame "left" et une frame "right".
            La frame "left" contient un widget "Pastchoice" qui permet à l'utilisateur de naviguer parmi les images
            déjà traitées.
            La frame "right" contient une sous-frame "top" et une sous-frame "btm". La sous-frame "top" est utilisée
            pour afficher les images
            traitées et la sous-frame "btm" contient un slider, un label et un bouton de validation.

            Returns:
                None
            """
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=5, uniform="group1")
        self.grid_rowconfigure(0, weight=1)
        right = tk.Frame(self)
        left = tk.Frame(self)
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
        btm.columnconfigure(3, weight=1, uniform="group2")
        self.end_btn = ctk.CTkButton(btm, text="Validation finale", command=self.end)
        self.end_btn.grid(row=0, column=3)
        next_btn = ctk.CTkButton(btm, text="Next", command=self.next)
        next_btn.grid(row=0, column=2)

        for r in range(Application.row):
            top.grid_rowconfigure(r, weight=1)
            if r == 0:
                pady = (10, 5)
            elif r == Application.row:
                pady = (5, 10)
            else:
                pady = (5, 5)
            for c in range(Application.col):
                if c != 0:
                    padx = (5, 5)
                elif c == Application.col:
                    padx = (5, 10)
                else:
                    padx = (10, 5)
                top.grid_columnconfigure(c, weight=1, uniform="group1")
                Application.photo_frame[r][c] = {
                    'btn': ctk.CTkButton(top, fg_color="grey", hover_color="palegreen",
                                         command=lambda coords=(r, c): self.button_click(coords), text="_"),
                    'clicked': False, 'order': None, 'source': ""}
                Application.photo_frame[r][c]['btn'].grid(row=r, column=c, sticky="nsew", padx=padx, pady=pady)
                w, h = get_frame_size(right)
                w = w // Application.col + 1
                h = h // Application.row + 1
                Application.size_photo = (w, h)
        self.new_image()


    def button_click(self, coords):
        """Change l'état d'un bouton de photo lorsqu'il est cliqué.

                Args:
                    coords (tuple): Les coordonnées du bouton de photo cliqué.

                Returns :
                    None
        """
        r = coords[0]
        c = coords[1]
        focus_btn = self.photo_frame[r][c]
        if focus_btn["clicked"]:
            focus_btn['btn'].configure(fg_color="grey")
            focus_btn['clicked'] = False
            Application.selected_source["source"].pop(f"{r}_{c}")
        else:
            #self.unselect_all()
            focus_btn['btn'].configure(fg_color="darkgreen")
            focus_btn['clicked'] = True
            Application.selected_source["source"][f"{r}_{c}"] = focus_btn["source"]

    def next(self):
        self.unselect_all()
        f = list(Application.selected_source["source"].values())
        self.end_btn.configure(state="normal")
        Application.selected_source["thumbnail"] = make_thumbnail(f)
        self.scroll_left.add_img((self.w_past, self.h_past))
        change_temp(list(Application.selected_source["source"].values()))
        Application.new_image()
        Application.selected_source["source"] = {}

    def unselect_all(self):
        """
            Désélectionne tous les boutons de l'image.

            Parcourt la grille de boutons de l'image et désélectionne chacun d'eux, en
            changeant leur couleur de police en gris et en marquant le bouton comme non
            cliqué.

        """
        for r in range(Application.row):
            for c in range(Application.col):
                self.photo_frame[r][c]['btn'].configure(fg_color="grey")
                self.photo_frame[r][c]['clicked'] = False

    def valid_choice(self):
        pass

    @classmethod
    def new_image(cls):
        """
        Génère de nouvelles images pour chaque bouton de la grille photo.

            Args:
                Aucun.

            Returns:
                Aucun.
        """
        cls.unselect_all(cls)
        if Application.never:
            for i in range(1, 6):
                shutil.copyfile(f"dataset/00000/0000{i}.png", f"{muted_path}0000{i}.png")
        else:
            ae.main_genetic_algorithm()
        Application.never = False
        if Application.never:
            for r in range(Application.row):
                for c in range(Application.col):
                    source = random_img()
                    Application.photo_frame[r][c]['source'] = source
                    Application.photo_frame[r][c]['btn'].configure(
                        image=convert_photoimg(source, Application.size_photo),
                        compound='top')
        else:
            source = created_img()
            for r in range(Application.row):
                for c in range(Application.col):
                    Application.photo_frame[r][c]['source'] = source[r - 1][c - 1]
                    Application.photo_frame[r][c]['btn'].configure(
                        image=convert_photoimg(source[r - 1][c - 1], Application.size_photo),
                        compound='top')

    def end_gif(self):
        self.toplevel = tk.Toplevel(self)
        self.toplevel.grid_columnconfigure(0, weight=1, uniform="group1")
        self.toplevel.grid_rowconfigure(0, weight=1, uniform="group1")
        self.gif_frame = ctk.CTkButton(self.toplevel, image=convert_photoimg("gif/output_0.png", None),
                                       compound="bottom",
                                       text="next", command=self.end_anim, fg_color="darkgrey", hover_color="grey")
        self.gif_frame.grid(row=0, column=0)
        im = "gif/police-dance.gif"
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except ValueError:
            self.delay = 100

        if len(frames) == 1:
            self.gif_frame.configure(image=next(self.frames))
        else:
            self.next_frame()

    def next_frame(self):
        if self.frames:
            self.gif_frame.configure(image=next(self.frames))
            self.after(self.delay, self.next_frame)

    def end_anim(self):
        self.gif_frame.configure(image=None)
        self.frames = None
        self.gif_frame.destroy()
        self.toplevel.destroy()
        global fun
        fun = False
        self.end()

    def end(self):
        if fun:
            self.end_gif()
        else:
            # ajouter verif de si ca vous va
            self.toplevel = tk.Toplevel(self)
            self.toplevel.grid_columnconfigure(0, weight=1, uniform="group1")
            self.toplevel.grid_rowconfigure(0, weight=1, uniform="group1")
            export_image = ctk.CTkButton(self.toplevel,
                                         image=ImageTk.PhotoImage(Image.open(Application.selected_source)),
                                         compound="bottom",
                                         text="export image", fg_color="darkgrey", hover_color="grey")
            export_image.grid(row=0, column=0)


for dir_path in [last_path, muted_path, past_temp, muted_path, dir_cache]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)

app = Application()
# Load the image file from disk.
icon = tk.PhotoImage(file=".source/logo.png")
# Set it as the window icon.
app.iconphoto(True, icon)
app.mainloop()
