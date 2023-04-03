import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk
import glob
from itertools import count, cycle
import shutil
import os
from PIL import Image
from AE_GEN import autocode, main_genetic_algorithm, main_autocodeur
import numpy as np
from pdf import main_pdf, make_qr
import uuid
import random
import string
from math import ceil, sqrt
from datetime import datetime
import json
from tkinter.filedialog import asksaveasfile
import sys

img_path = ".data/00000/"
last_path = ".past/"
muted_path = ".img/"
past_temp = ".past_temp/"
dir_cache = ".cache/"
fun = False# Fun mode
json_make = False # Make a json recap
db_autocoded = True # Autoencode les images de la database
f = open('../params.json')

# returns JSON object as
# a dictionary
params = json.load(f)
H = params["H"]  # Hauteur des images
W = params["W"]  # Largeur des images
C = params["C"]  # 3 si RGB 1 si N&B


def rdm_le(x: int, majuscule: bool) -> str:
    """
        Génère une chaîne de caractères aléatoire de longueur x en utilisant des lettres majuscules ou minuscules.

        Args:
            x (int): Longueur de la chaîne de caractères à générer.
            majuscule (bool): Si True, les lettres générées sont en majuscules. Sinon, elles sont en minuscules.

        Returns :
            str : La chaîne de caractères générée.
        """
    if majuscule:
        return random.choice(string.ascii_uppercase)[:x]
    else:
        return random.choice(string.ascii_lowercase)[:x]


def export_pdf(value, hist_list, end_path, json_):
    """
        Exporte les données du dictionnaire `value` sous forme de fichier PDF.

        Args:
            value (dict): Dictionnaire contenant les données à exporter sous forme de PDF.
            hist_list (list) : Liste d'images à inclure dans le PDF.
            end_path (str) : Chemin de destination pour les fichiers exportés.
            json_ (bool): Si `True`, les données sont également sauvegardées sous forme de fichier JSON.

        Returns:
            None
    """
    id = value["rapport"]
    make_qr(id)
    hist_img = Make_thumbnail(hist_list, 255)
    path = [end_path, hist_img, "qr_code.png"]
    if json_:
        file_json = asksaveasfile(filetypes=[('json Files', '*.json')])
        """
        value["Portrait_robot"] = asarray(Image.open(end_img)).tolist()
        value["History"] = asarray(Image.open(hist_img)).tolist()
        value["qr_code"] = asarray(Image.open("qr_code.png")).tolist()
        """
        with open(file_json.name, 'w') as outfile:
            outfile.write(json.dumps(value))
    file_pdf = asksaveasfile(filetypes=[('pdf Files', '*.pdf')])
    for i, p in enumerate(path):
        if isinstance(p, list):
            path[i] = p[0]
    main_pdf(value, path, file_pdf.name)
    app.quit()


def Make_thumbnail(list_img, color=0):
    """Crée un assemblage de la liste d'images spécifiée par leurs path et la sauvegarde dans un fichier
    nommé "thumbnailed.png".

    Args:
        list_img (list): Une liste d'images à utiliser pour créer la miniature.
        color (int): valeur des pixels par défauts

    Returns:
        str: Le chemin du fichier "thumbnailed.png" créé.

    Raises:
        Aucune erreur n'est levée dans cette fonction.
    """
    N = len(list_img)
    x = ceil(sqrt(N))
    c = 0
    r = 0
    collage = Image.new('RGB', (W * x, H * x), color=(color, color, color))
    for i in list_img:
        if c == x:
            c = 0
            r += 1
        collage.paste(Image.open(i).resize((H, W)), (W * c, H * r))
        c += 1

    collage.save(f"{dir_cache}thumbnailed.png")

    return f"{dir_cache}thumbnailed.png"


def init_dict(nb_row, nb_col):
    """Initialise un dictionaire python avec des Nones de la forme :
        {"R": {"C" : None} * x } * y --> Tableau 2D
    avec x = nb_col, y = nb_row et C et R des entiers de 0 au nombre maximal.
    Args:
        nb_row (int) : Nombre de "ligne"
        nb_col (int) : Nombre de "colonne"
    Returns:
        dict_ (dict) : Dictionaire
    """
    dict_ = {}
    for r in range(nb_row):
        dict_[r] = {}
        for c in range(nb_col):
            dict_[r][c] = None
    return dict_


def change_temp(files, dir_clean=past_temp, dir_dest=past_temp):
    """Suprimme les fichiers stocker dans past_temp et place dans ce dossier la derniere generation d'images choisie

    Args:
        files (list) : Liste avec les paths des images de la derniere generation
        dir_clean (str) : Path vers le dossier à vider
        dir_dest (str) : PAth vers le dossier à remplir
    """
    for d in os.listdir(dir_clean):
        os.remove(f"{dir_clean}{d}")
    for f in files:
        shutil.copyfile(f, f"{dir_dest}/{f.split('/')[-1]}")


def random_img(dir_choice=img_path):
    """
        Retourne une image aléatoire parmi les images dans dir_choice.
        Args:
            dir_choice (str) : Chemin vers le dossier avec les images
        Returns:
            random_image (str) : Chemin d'accès vers l'image aléatoire sélectionnée.
        """
    images = glob.glob(random.choice([dir_choice + "*.png"]))
    random_image = random.choice(images)
    return random_image


def created_img(bl=db_autocoded):
    """Recupere dans files la liste des path des images dans muted_path. Reforme la liste sous la forme
    2 ligne 3 colonnes
    Args :
        bl (bool): l'image supplementaire de la base de donnée doit-elle passer par l'autoencodeur
    Returns:
        img_lst (list) : Liste des path d'image dans muted_path sous la forme [2][3]
    """
    liste = os.listdir(muted_path)
    files = []
    for l in liste:
        if l[0] != '.':
            files.append(l)
    for i, f in enumerate(files):
        files[i] = f"{muted_path}{f}"
    path = random_img()
    autocoded = autocode(path, encoder, decoder, bl)
    files.append(autocoded)
    arr_img = np.array(files)
    img_lst = arr_img.reshape(2, 3)
    return img_lst


def get_frame_size(frame):
    """
    Récupère la taille d'un cadre.

    Args:
        frame (Tkinter.Frame): Cadre dont la taille doit être récupérée.

    Returns:
        w: Largeur de frame.
        h: Hauteur de frame
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
            photo_image (tkinter.PhotoImage): Objet PhotoImage de l'image convertie et redimensionnée.
        """
    if size is None:
        photo_image = ctk.CTkImage(light_image=Image.open(source), dark_image=Image.open(source))
    else:
        photo_image = ctk.CTkImage(light_image=Image.open(source), dark_image=Image.open(source),
                                   size=(size[0], size[1]))
    return photo_image


class Pastchoice(ctk.CTkScrollableFrame):
    """Classe qui représente la liste des choix de photos passés de l'application.

        Hérite de ctk.CTkScrollableFrame.

        Attributs :
            count (int) : Le nombre de générations précédentes.
            all_past (dict) : Un dictionnaire contenant tous les boutons d'images précédents et leurs chemins associés.

        Méthodes :
            add_img : Ajoute une image à l'interface graphique sous forme de bouton avec un texte et un compteur.
            go_past : Efface tous les boutons d'images qui se trouvent après le bouton sélectionné.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.count = 0  # Nombre de generation précédentes
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
        for source_img in list(Application.selected_source["source"].values()):
            end_path = source_img.split("/")[1]
            new_path = new_dir + end_path
            shutil.copyfile(source_img, new_path)
            shutil.copyfile(source_img, f"{past_temp}{end_path}")
        old = ctk.CTkButton(self, fg_color="grey", hover_color="palegreen",
                            command=lambda cnt=self.count, source=Application.selected_source["source"]: self.go_past(
                                cnt),
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
        files = {}
        for i, f in enumerate(os.listdir(f"{last_path}{self.count}")):
            files[i] = f"{last_path}{self.count}/{f}"
        change_temp(list(files.values()))
        Application.selected_source["source"] = files
        Application.new_image()


def get_history():
    """
    Récupère la liste complète de l'historique des sources stockées dans le dossier last_path.

    Returns:
        h list : Une liste des chemins d'accès complets à tous les fichiers d'historique.
    """
    h = []
    for d in range(1, len(os.listdir(last_path)) + 1):
        for i in os.listdir(f"{last_path}{d}"):
            h.append(f"{last_path}{d}/{i}")
    return h


def get_coupable_list():
    """
    Récupère la liste des coupables sélectionnés dans l'application.

    Returns:
        coupable_list (list) : La liste des coupables sélectionnés.
    """
    coupable_list = list(Application.selected_source["source"].values())
    return coupable_list


class Application(ctk.CTk):
    """Classe principale de l'application qui étend la boîte à outils graphique ctk.CTk.

        Attributs :
            size_photo (None) : La taille de la photo à générer.
            selected_source (dict) : La source sélectionnée pour la photo, contenant une miniature et une source.
            report (dict) : Le rapport d'utilisation de l'application, contenant un historique et une date de fin.
            never (True) : Indique si une génération d'image a déjà eu lieu.
            col (3) : Le nombre de colonnes dans le cadre de la photo.
            row (2) : Le nombre de lignes dans le cadre de la photo.
            photo_frame (dict) : Un dictionnaire représentant le cadre de la photo, initialisé avec des valeurs par défaut.

        Méthodes :
            __init__ : Initialise une nouvelle instance de l'application avec des valeurs par défaut.
            info : Affiche les informations de l'application.
            make_frame : Crée le cadre de la photo.
            enter_info : Permet à l'utilisateur d'entrer des informations pour le rapport d'utilisation de l'application.
        """
    size_photo = None
    selected_source = {"thumbnail": "", "source": {}}
    report = {"history": [], "end": ""}
    never = True  # Y a t-il deja eu une generation  d'image
    col = 3
    row = 2
    photo_frame = init_dict(row, col)

    def __init__(self):
        super().__init__()
        self.info_entry = None
        self.delay = None
        self.value = {"rapport": f"{rdm_le(1, True)}{str(uuid.uuid4())[:3]}{rdm_le(1, False)}{str(uuid.uuid4())[:4]}",
                      "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "auteur": "", "victime": "", "enquete": "",
                      "remarque_enquete": "", "remarque_photo": ""}

        self.toplevel = None
        self.end_btn = None
        self.h_past = None
        self.w_past = None
        self.remarque_txt = None
        self.scroll_left = None
        self.entropy_slider = None
        self.entropy_value = None
        self.gif_frame = None
        self.frames = None
        self.title("zero")
        self.info()
        self.make_frame()
        self.enter_info()

    def enter_info(self):
        """
            Affiche une fenêtre Toplevel pour permettre à l'utilisateur de saisir les informations concernant l'auteur,
            la victime et le numéro d'enquête. Les informations sont saisies dans des Entry.
            """
        self.withdraw()
        frame_info = tk.Toplevel(self)
        frame_info.title("Enter info")
        frame_info.update()
        frame_info.geometry("+%d+%d" % ((self.winfo_screenwidth() // 2) - (frame_info.winfo_width() // 2),
                                        (self.winfo_screenheight() // 2) - (frame_info.winfo_height() // 2)))
        frame_info.grid_columnconfigure(0, weight=1, uniform="group1")
        frame_info.grid_columnconfigure(1, weight=1, uniform="group1")
        frame_info.grid_rowconfigure(0, weight=1, uniform="group1")
        frame_info.grid_rowconfigure(1, weight=1, uniform="group1")
        frame_info.grid_rowconfigure(2, weight=1, uniform="group1")
        frame_info.grid_rowconfigure(3, weight=1, uniform="group1")
        auteur_L = ctk.CTkLabel(frame_info, text="Auteur")
        auteur_L.grid(row=0, column=0)
        auteur_E = ctk.CTkEntry(frame_info, placeholder_text="Auteur")
        auteur_E.grid(row=0, column=1)
        vic_L = ctk.CTkLabel(frame_info, text="Victime")
        vic_L.grid(row=1, column=0)
        vic_E = ctk.CTkEntry(frame_info, placeholder_text="Victime")
        vic_E.grid(row=1, column=1)
        enq_L = ctk.CTkLabel(frame_info, text="Enquete n°")
        enq_L.grid(row=2, column=0)
        enq_E = ctk.CTkEntry(frame_info, placeholder_text="Enquete n°")
        enq_E.grid(row=2, column=1)
        self.info_entry = [frame_info, auteur_E, vic_E, enq_E]
        val_btn = ctk.CTkButton(frame_info, text="Validation", command=lambda: self.start_choice())
        val_btn.grid(row=3, column=0, columnspan=2)

    def start_choice(self):
        """
            Récupère les informations sur l'auteur, la victime et l'enquête saisies par l'utilisateur,
            détruit le widget d'entrée de ces informations et affiche l'interface principale de l'application.

            Returns:
                None
            """
        val = ["auteur", "victime", "enquete"]
        for i, e in enumerate(self.info_entry[1:]):
            self.value[val[i]] = str(e.get())
        self.info_entry[0].destroy()
        self.deiconify()
        self.info()

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
                # TODO implementer le double click qui déclanche unselect_all
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
            focus_btn['btn'].configure(fg_color="darkgreen")
            focus_btn['clicked'] = True
            Application.selected_source["source"][f"{r}_{c}"] = focus_btn["source"]

    def next(self):
        """
        Déselectionne toutes les images sélectionnées. Si au moins une image était sélectionnée,
        met le bouton "End" dans l'état "normal", crée une miniature de l'image sélectionnée et ajoute cette miniature
        à la barre de défilement. Change le dossier actuel en fonction de la ou des images sélectionnées,
        puis charge une nouvelle image. Réinitialise le dictionnaire "source" à une valeur vide.


        Returns:
            None
        """
        min_one = False
        for r in self.photo_frame.values():
            for c in r.values():
                if c["clicked"]:
                    min_one = True
                    break

        if min_one:
            self.unselect_all()
            f = list(Application.selected_source["source"].values())
            self.end_btn.configure(state="normal")
            Application.selected_source["thumbnail"] = Make_thumbnail(f)
            self.scroll_left.add_img((self.w_past, self.h_past))
            change_temp(list(Application.selected_source["source"].values()))
            Application.new_image()
            Application.selected_source["source"] = {}
            # TODO resoudre warning Expected type 'dict', got 'Dict[str, Union[str, Any]]' instead

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
                shutil.copyfile(random_img(img_path), f"{muted_path}0000{i}.png")
            source = created_img(False)
            Application.never = False
        else:
            main_genetic_algorithm(encoder, decoder)
            source = created_img()
        for r in range(Application.row):
            for c in range(Application.col):
                Application.photo_frame[r][c]['source'] = source[r - 1][c - 1]
                Application.photo_frame[r][c]['btn'].configure(
                    image=convert_photoimg(source[r - 1][c - 1], Application.size_photo),
                    compound='top')

    def end_gif(self):
        """
            Ouvre une fenêtre Toplevel qui affiche un bouton avec le premier frame de la vidéo GIF.
            Lorsque l'utilisateur clique sur le bouton, le frame suivant est affiché jusqu'à la fin de la vidéo.
            À la fin de la vidéo, la fenêtre Toplevel est détruite et la méthode end_anim() est appelée.

            Returns:
                None
            """
        self.toplevel = tk.Toplevel(self)
        self.toplevel.grid_columnconfigure(0, weight=1, uniform="group1")
        self.toplevel.grid_rowconfigure(0, weight=1, uniform="group1")
        self.gif_frame = ctk.CTkButton(self.toplevel, image=convert_photoimg(".data/gif/output_0.png", None),
                                       compound="bottom",
                                       text="next", command=self.end_anim, fg_color="darkgrey", hover_color="grey")
        self.gif_frame.grid(row=0, column=0)
        im = ".data/gif/police-dance.gif"
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
        """
            Affiche la prochaine image de la liste frames et planifie un rappel pour afficher la suivante après un délai

            Returns:
                 None
            """
        if self.frames:
            self.gif_frame.configure(image=next(self.frames))
            self.after(self.delay, self.next_frame)

    def end_anim(self):
        """
            Supprime l'affichage de la fenêtre de sélection et détruit tous les éléments associés.
            Définit également la variable globale fun à False.

            Returns:
                 None
            """
        self.gif_frame.configure(image=None)
        self.frames = None
        self.gif_frame.destroy()
        self.toplevel.destroy()
        global fun
        fun = False
        self.end()

    def Subselect(self, coupable):
        """
           Sélectionne une source spécifique à partir d'une liste de sources et enregistre le choix dans le rapport
           d'application.

           Args:
            coupable (str): Le chemin d'accès complet à la source sélectionnée.
           Returns:
                None
           """
        Application.report["end"] = coupable
        Application.report["history"] = get_history()
        for i in list(Application.selected_source["source"].values()):
            if i != coupable:
                Application.report["history"].append(i)
        self.save_coupable()

    def Subselect_top(self, sub_list):
        """
            Affiche une fenêtre de sélection pour une liste de sources.

            Args:
             sub_list (list) : La liste des chemins d'accès complets des sources sélectionnables.
            Returns:
                 None
            """
        top = tk.Toplevel(self)
        top.title("SubSelect")
        for i in sub_list:
            export_image = ctk.CTkButton(top,
                                         image=ImageTk.PhotoImage(Image.open(i)),
                                         compound="bottom", command=lambda x=i: self.Subselect(x),
                                         text="export image", fg_color="darkgrey", hover_color="grey")
            export_image.pack()

    def end_in(self, source):
        """
            Sélectionne une source si une seule est disponible, sinon appelle la méthode Subselect_top() pour
            afficher une sous-sélection de sources.

            Args:
             source (list): Une liste de sources à sélectionner.
            Returns:
                 None
            """
        if len(source) > 1:
            self.Subselect_top(source)
        else:
            Application.report["end"] = source
            Application.report["history"] = get_history()
            self.save_coupable()

    def end_out(self):
        """
        Affiche une sélection d'historiques et enregistre l'historique sélectionné dans le rapport d'application.

        Returns:
             None
        """
        past_path = os.listdir(past_temp)
        if len(past_path) > 1:
            temp = []
            for f in past_path:
                temp.append(f"{past_temp}{f}")
            self.Subselect_top(temp)
        else:
            Application.report["end"] = F"{past_temp}{past_path[0]}"
            Application.report["history"] = get_history()
            self.save_coupable()

    def end(self):
        """
            Vérifie si des coupables ont été sélectionnés dans les 6 proposé et appelle la méthode end_in() si c'est
            le cas, sinon appelle la méthode end_out().

            Returns:
                 None
            """
        if fun:
            self.end_gif()
        else:
            source_list = get_coupable_list()
            if len(source_list) == 0:  # cas pas dans les 6
                self.end_out()
            else:
                self.end_in(source_list)

    def save_coupable(self):
        """
        Fonction qui enregistre le rapport final et ouvre une fenêtre de saisie de remarques.

        Args:
            Aucun.

        Returns:
            None
        """
        hist_ = Application.report["history"]
        coupable_ = Application.report["end"]
        rem = tk.Toplevel(self)
        rem.title("Remarques")
        rem.update()
        rem.geometry("+%d+%d" % ((self.winfo_screenwidth() // 2) - (rem.winfo_width() // 2),
                                 (self.winfo_screenheight() // 2) - (rem.winfo_height() // 2)))
        rem.grid_columnconfigure(0, weight=1, uniform="group1")
        rem.grid_rowconfigure(0, weight=1)
        rem.grid_rowconfigure(1, weight=1)
        self.remarque_txt = tk.Text(rem)
        self.remarque_txt.grid(row=0, column=0, sticky="nsew")
        val_btn = ctk.CTkButton(rem, text="Validation",
                                command=lambda h=hist_, c=coupable_, b=json_make: self.call_export(h, c, b))
        val_btn.grid(row=1, column=0)

    def call_export(self, h, c, b):
        """
            Fonction qui prépare les données pour l'export PDF et appelle la fonction d'export.

            Args:
                h (int): Hauteur de la photo à exporter.
                c (int): Largeur de la photo à exporter.
                b (str): Chemin d'accès du fichier de destination pour l'export.

            Returns:
                None
            """
        txt = self.remarque_txt.get("1.0", "end-1c").split()
        new_txt = []
        line = ""
        line_count = 0
        for word in txt:
            longeur = len(line)
            ll = len(word)
            if longeur + ll >= 25:
                new_txt.append(line)
                line_count += 1
                line = word
            else:
                line += f" {word}"
        new_txt.append(line)
        self.value["remarque_photo"] = new_txt
        export_pdf(self.value, h, c, b)


if __name__ == '__main__':
    for dir_path in [last_path, muted_path, past_temp, muted_path, dir_cache]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            shutil.rmtree(dir_path)
            os.makedirs(dir_path)
    global encoder
    global decoder
    encoder, decoder = main_autocodeur()
    app = Application()
    # Load the image file from disk.
    icon = tk.PhotoImage(file=".source/logo.png")
    # Set it as the window icon.
    app.iconphoto(True, icon)
    app.mainloop()
    print("Application closed")
