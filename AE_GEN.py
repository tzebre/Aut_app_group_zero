import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from sklearn.model_selection import train_test_split
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Conv2D, Activation, MaxPool2D
from tensorflow.keras.layers import BatchNormalization, Flatten, Reshape, Conv2DTranspose, LeakyReLU
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam, SGD

print("")
t = 64
from tqdm import trange, tqdm

##ajouté pour algo gen
from statistics import mean
from random import *

## Seeding
np.random.seed(42)
tf.random.set_seed(42)

H = 64
W = 64
C = 3

## réutiliser les modèles sauvegardés
encoder = tf.keras.models.load_model('saved_model/encoder.tf', compile=False)
decoder = tf.keras.models.load_model('saved_model/decoder.tf', compile=False)

encoder.compile(optimizer=Adam(1e-3), loss='binary_crossentropy')
decoder.compile(optimizer=Adam(1e-3), loss='binary_crossentropy')


## ouvrir les images d'un dossier

def open_dir():
    X = []
    for file in os.listdir("dataset/06000"):
        img = Image.open(f"dataset/06000/{file}")
        img = img.resize((t, t))
        arr = np.array(img) / 255
        X.append(arr)
    X = np.array(X)
    return (X)


def convert_img(img_path):
    img = Image.open(img_path)
    img = img.resize((t, t))
    arr = np.array(img) / 255
    return (np.array([arr]))

def plot_img(data,decoded):
  n = len(data) ## how many digits we will display
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

def mutate_arr(array, r):
    encoded = encoder.predict(array)
    print(encoded.shape)
    v = np.copy(encoded)
    for i in range(len(v)):  ##pour chaque image
        moyenne = mean(v[i])
        sigma = np.std(v[i])
        ## à faire varier : le nombre devant sigma + la proba avec laquelle il y a des mutations
        for j in range(len(v[i])):
            p = np.random.random()
            if p < r:
                # print('mutation')
                v[i, j] = 1 * sigma * np.random.random() + moyenne
    return v
def mutation(data_encoded,r): # proba mutation
  v = np.copy(data_encoded)
  for i in range(len(v)): ##pour chaque image
    moyenne=mean(v[i])
    sigma=np.std(v[i])
    ## à faire varier : le nombre devant sigma + la proba avec laquelle il y a des mutations
    for j in range(len(v[i])):
      p = np.random.random()
      if p < r:
        #print('mutation')
        v[i,j] = 1*sigma*np.random.random()+moyenne
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




if __name__ == "__main__":
    X = open_dir()
    data = X[0:6]
    print(data.shape)
    encoded_imgs = encoder.predict(data)
    decoded_imgs = decoder.predict(encoded_imgs)
    plot_img(data, decoded_imgs)
    v = encoder.predict(data)
    mutated = mutation(v, 0.3)
    dec_mut = decoder.predict(mutated)
    plot_img(decoded_imgs, dec_mut)
    v = encoder.predict(data)
    newv = crossing_over(v, 0.5)
    # print(v[0]==newv[0]) ##ok
    dec_cross = decoder.predict(newv)
    # print(decoded_imgs[0]==dec_cross[0])
    plot_img(decoded_imgs, dec_cross)
    newv2 = crossing_over(v, 0.2)
    dec_cross2 = decoder.predict(newv2)
    plot_img(decoded_imgs, dec_cross2)
    cm = crossing_over(v, 0.2)
    cm = mutation(cm, 0.3)
    dec_cm = decoder.predict(cm)
    plot_img(decoded_imgs, dec_cm)
    mc = mutation(v, 0.3)
    mc = crossing_over(mc, 0.2)
    mc2 = mutation(mc, 0.2)
    mc2 = crossing_over(mc2, 0.3)
    dec_mc = decoder.predict(mc2)
    plot_img(decoded_imgs, dec_mc)

