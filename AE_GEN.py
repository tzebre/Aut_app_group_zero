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

H = 64
W = 64
C = 3
encoder = tf.keras.models.load_model('saved_model/encoder.tf', compile=False)
# encoder.summary()
decoder = tf.keras.models.load_model('saved_model/decoder.tf', compile=False)
# decoder.summary()

encoder.compile(optimizer=Adam(1e-3), loss='binary_crossentropy')
decoder.compile(optimizer=Adam(1e-3), loss='binary_crossentropy')


# plot(data,decoded_imgs)
def implement_img():
    """
    Returns:
      a tab of the encoded selected images
    """
    X = []
    # for file in os.listdir(f"dataset/06000"):
    if len(os.listdir(f".past_temp/")) != 0:
        for file in os.listdir(f".past_temp/"):
            if file != ".DS_Store":
                # img = Image.open(f"dataset/06000/{file}")
                img = Image.open(f".past_temp/{file}")
                t = 64
                img = img.resize((t, t))
                arr = np.array(img) / 255
                X.append(arr)
    else:
        for file in os.listdir(f"dataset/06000/"):
            if file != ".DS_Store":
                img = Image.open(f"dataset/06000/{file}")
                t = 64
                img = img.resize((t, t))
                arr = np.array(img) / 255
                X.append(arr)
    X = np.array(X)
    X = encoder.predict(X)

    return X


X = implement_img()[0:6]
print(len(X))


# print(X[0:6])

def generate_initial_pop(list_img, N):
    """
    Args:
      list_img : a list of encoded images
    Return:
      initial population of genetic algorithm
    """
    res = []
    #  N=len(list_img)
    # print(N)
    val = (1, 1, 1)
    if N == 1:
        for i in (0, 0, 0, 0, 0):
            res.append(list_img[0])
            val = (0.3, 1, 0.6)
    elif N == 2:
        for i in (0, 0, 0, 1, 1):
            res.append(list_img[i])
            val = (0.3, 0.9, 0.6)
    elif N == 3:
        for i in (0, 0, 1, 1, 2):
            res.append(list_img[i])
            val = (0.3, 0.8, 0.7)
    elif N == 4:
        for i in (0, 0, 1, 2, 3):
            res.append(list_img[i])
            val = (0.3, 0.6, 0.7)
    elif N == 5:
        for i in (0, 1, 2, 3, 4):
            res.append(list_img[i])
            val = (0.2, 0.6, 0.8)

    # print(len(res))
    return (np.array(res), val)


def mutation(data_encoded, r, ratio=1):
    v = np.copy(data_encoded)
    for i in range(len(v)):  ##pour chaque image
        moyenne = mean(v[i])
        sigma = np.std(v[i])
        # print("vecteur")
        # print(v[i])
        print(moyenne)
        print(sigma)
        ## à faire varier : le nombre devant sigma + la proba avec laquelle il y a des mutations
        for j in range(len(v[i])):
            p = np.random.random()
            if p < r:
                # print('mutation')
                a = np.random.random()
                if a < 0.5:
                    v[i, j] = ratio * 1 * sigma * np.random.random() + moyenne
                else:
                    v[i, j] = ratio * -1 * sigma * np.random.random() + moyenne
    return v


def crossing_over(P, Tc):
    new_P = np.copy(P)

    for i in range(0, len(new_P)):  # pour chaque individu
        if random() < Tc:
            print("crosing over")
            indc = randint(0, new_P.shape[0] - 1)  # entier aleat entre 0 et nb d'individus dans la pop
            while indc == i:
                indc = randint(0, new_P.shape[0] - 1)
            posc = randint(0, new_P.shape[1] - 1)  # entier aleat entre 0 et nb de gènes dans chaque individu
            # posc = 32
            # print(i)
            # print(indc)
            # print(posc)
            # print()
            ## np.copy pour avoir deep copy!!
            tmp = np.copy(new_P[i, posc:new_P.shape[
                1]])  # tmp valeurs de new P de l'individu sur lequel on est (i), gènes après posc
            new_P[i, posc:new_P.shape[1]] = np.copy(
                new_P[indc, posc:new_P.shape[1]])  # individu i après posc prend les valeurs de l'indiv indc après posc
            new_P[indc, posc:new_P.shape[1]] = tmp  # individu insc prend valeurs indiv i après posc
    return new_P


def plot_img(data, decoded):
    n = len(data)  ## how many digits we will display
    plt.figure(figsize=(20, 4))
    for i in range(n):
        ## display original
        ax = plt.subplot(2, n, i + 1)
        ax.set_title("Original Image")
        plt.imshow(data[i].reshape(H, W, C))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ## display reconstruction
        ax = plt.subplot(2, n, i + 1 + n)
        ax.set_title("Predicted Image")
        plt.imshow(decoded[i].reshape(H, W, C))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.show()


# Afficher chaque image et les enregistrer en PNG
def save_modified_img(pop):
    # rajouter les points après
    if not os.path.exists('.img'):
        os.makedirs('.img')
    else:
        shutil.rmtree('.img')
        os.makedirs('.img')

    for i in range(pop.shape[0]):
        plt.imshow(pop[i])
        plt.axis('off')

        # Redimensionner l'image en 64x64 pixels
        img = Image.fromarray(np.uint8(pop[i] * 255))
        # img = img.resize((64, 64))

        # Enregistrer l'image en tant que fichier PNG
        path = f".img/muted_{time.time()}.png"
        img.save(path, format='PNG', dpi=(300, 300))

        plt.clf()  # Effacer la figure pour la prochaine image


def main_genetic_algorithm():
    images = implement_img()[0:4]
    N = len(images)
    if N == 64:
        images = [images]
        N = len(images)
    pop, val = generate_initial_pop(images, N)
    # plot_img(decoder.predict(pop),decoder.predict(pop))
    # print(len(pop))
    # pop=generate_initial_pop(images)
    r_mut = val[0]
    ratio = val[1]
    r_cross = val[2]
    pop = mutation(pop, r_mut, ratio)  # d'abord faire mutations sinon crossing over sert à rien
    pop = crossing_over(pop, r_cross)
    # print(len(pop))

    pop = decoder.predict(pop)
    #plot_img(pop, pop)

    save_modified_img(pop)

#main_genetic_algorithm()
