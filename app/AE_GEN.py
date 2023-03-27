import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras.optimizers import Adam, SGD

import time
import shutil

##ajouté pour algo gen
from statistics import mean
from random import *

## Seeding
np.random.seed(42)
tf.random.set_seed(42)
img_path = ".data/00000/"

H = 128
W = 128
C = 3
encoder = tf.keras.models.load_model('model/encoder_128.tf', compile=False)
# encoder.summary()
decoder = tf.keras.models.load_model('model/decoder_128.tf', compile=False)
# decoder.summary()

encoder.compile(optimizer=Adam(1e-3), loss='binary_crossentropy')
decoder.compile(optimizer=Adam(1e-3), loss='binary_crossentropy')

def autocode(img, bl=True):
    img = Image.open(img)
    if bl:
        t = 128
        img = img.resize((t, t))
        array_img = np.array([np.array(img)/255])
        img = encoder.predict(array_img)
        img = decoder.predict(img)
        img = Image.fromarray(np.uint8(img[0] * 255))
    path = f".cache/autocode.png"
    img.save(path)
    return path

def implement_img():
    """Récupère les images sélectionnées et les encode
    Returns:
        list_img (float[]): liste d'images encodées sous forme de vecteur de taille 128.
    """
    list_img = []
    # for file in os.listdir(f"dataset/06000"):
    if len(os.listdir(f".past_temp/")) != 0:
        for file in os.listdir(f".past_temp/"):
            if file != ".DS_Store":
                # img = Image.open(f"dataset/06000/{file}")
                img = Image.open(f".past_temp/{file}")
                t = 128
                img = img.resize((t, t))
                list_img.append(np.array(img) / 255)
    else:
        for file in os.listdir(f"{img_path}"):
            if file != ".DS_Store":
                img = Image.open(f"{img_path}{file}")
                t = 128
                img = img.resize((t, t))
                list_img.append(np.array(img) / 255)
    list_img = np.array(list_img)
    list_img = encoder.predict(list_img)

    return list_img





def generate_initial_pop(list_img, N):
    """Génerer une population à partir du nombre d'image qui ont été sélectionnées et instanciation des probabilités de mutation et crossing over 

    Args:
        list_img (float[]): liste d'images encodées sous forme de vecteur de taille 128.

    Returns:
        initial_pop : population intiale qui va être utilisée par l’algorithme génétique

    """
  
    pop = []
    val_proba = (1,1,1)
    if N == 1 :
        for i in (0,0,0,0,0) :
            pop.append(list_img[0])
            val_proba = (0.3, 1, 0.6)
    elif N == 2 :
        for i in (0,0,0,1,1):
            pop.append(list_img[i])
            val_proba = (0.3, 0.9, 0.6)
    elif N == 3 :
        for i in (0,0,1,1,2):
            pop.append(list_img[i])
            val_proba = (0.3, 0.8, 0.7)
    elif N == 4 :
        for i in (0,0,1,2,3):
            pop.append(list_img[i])
            val_proba = (0.3, 0.6, 0.7)
    elif N == 5 :
        for i in (0,1,2,3,4):
            pop.append(list_img[i])
            val_proba = (0.2, 0.6, 0.8)

    initial_pop = (np.array(pop),val_proba)

    return initial_pop


def mutation(data_encoded,proba,ratio=1):
    '''Partie de l'algorithme génétique qui va permettre de réaliser des SNP aléatoirement 

    Args :
        data_encoded (float[]): liste d'images encodées sous forme de vecteur de taille 128.
        proba (float): probabilité d'avoir une mutation.
        ratio (float, optional): coefficient multiplicateur pour réduir l'effet de la mutation, par défaut le ratio vaut 1.

    Returns:
        list_img (float[]): liste d'images encodées modifiées
    '''

    list_img = np.copy(data_encoded)
    for i in range(len(list_img)): ##pour chaque image
        moyenne = mean(list_img[i])
        sigma = np.std(list_img[i])

        for j in range(len(list_img[i])):
            p = np.random.random()

            if p < proba:
                random_value = np.random.random()

                if random_value < 0.5:
                    list_img[i,j] = ratio * 1 * sigma * np.random.random() + moyenne
              
                else:
                    list_img[i,j] = ratio * -1 * sigma * np.random.random() + moyenne

    return list_img


def crossing_over(data_encoded, Tc):
    '''Partie de l'algorithme génétique qui va permettre de réaliser des crossing over 

    Args :
        data_encoded (float[]): liste d'images encodées sous forme de vecteur de taille 128.
        Tc (float): probabilité d'avoir un crossing over.

    Returns:
        list_img (float[]): liste d'images encodées modifiées
    '''

    list_img = np.copy(data_encoded)
  
    for i in range(0,len(list_img)):
        if random() < Tc:
            random_indiv = randint(0, list_img.shape[0]-1) 
            while random_indiv == i:
                random_indiv = randint(0, list_img.shape[0]-1)

            position_cross = randint(0, list_img.shape[1]-1) 
         
            tmp = np.copy(list_img[i,position_cross:list_img.shape[1]]) 
            list_img[i,position_cross:list_img.shape[1]] = np.copy(list_img[random_indiv,position_cross:list_img.shape[1]]) 
            list_img[random_indiv,position_cross:list_img.shape[1]] = tmp 

    return list_img


def save_modified_img(pop):
    '''Sauvegarde les images au format PNG

    Agrs:
        pop (float[]): liste d'images decodées.
    '''
    if not os.path.exists('.img'):
        os.makedirs('.img')
    else:
        shutil.rmtree('.img')
        os.makedirs('.img')

    for i in range(pop.shape[0]):
        plt.imshow(pop[i])
        plt.axis('off')
        img = Image.fromarray(np.uint8(pop[i]*255))
        path = f".img/muted_{time.time()}.png"
        img.save(path, format='PNG', dpi=(300, 300))
        plt.clf()


def main_genetic_algorithm():
    '''Effectue la modification des images en utlisant un algorithme génétique

    Encode les images sélectionnées par l'utilisateur et va générer une population avec des probabilités qui lui sont propres.
    Modifie celle-ci au travers de mutation et de crossing over afin de générer une nouvelle population.
    Decode les images et les enregistre dans un dossier pour être lu par l'interface graphique.
    '''
    images=implement_img()

    nb_images = len(images)
    if nb_images == 64 :
        images = [images]
        nb_images = len(images)

    pop, val = generate_initial_pop(images, nb_images)

    proba_mut, ratio, proba_cross = val

    pop=mutation(pop,proba_mut,ratio) 
    pop=crossing_over(pop,proba_cross)

    pop=decoder.predict(pop)

    save_modified_img(pop)
