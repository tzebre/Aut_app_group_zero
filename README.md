
![image](https://user-images.githubusercontent.com/111517884/229428598-ba7af5ab-751c-484d-b192-2c05b21533e6.png)
# Notice d’utilisation Suspect authentificateur V1.0

Sommaire : 
#### 1. Lancement de l'application
##### 1.1. Installation, à faire lors de la première ouverture uniquement 
##### 1.2. Lancement de l'application pré-installée
#### 2. Vue globale de l'interface utilisateur 
#### 3. Un exemple d'utilisation pas à pas 
#### 4. Options supplémentaires
## Lancement de l'application

### Installation, à faire lors de la première ouverture uniquement : 

- 1. Ouvrir le terminal , aller dans le dossier *Aut_app_group_zero* : 
``` cd Aut_app_group_zero ```

- 2. Lancer le script .sh : 
```sh .instal/make_alias.sh ```
Un path apparaît :![image](https://user-images.githubusercontent.com/111517884/229459436-4d60c62f-acc4-4189-ac36-9931be5e3f61.png)
Il sert à créer un alias qui permettra de lancer l'application à l'aide d'une simple commande depuis n'importe où dans votre terminal. Copier le path alias : alias auth_app='source /Users/bacquiecamille/Documents/camille/4BIM/DVPT_logiciel/Aut_app_group_zero/execution.sh'

- 3. Ouvrer votre fichier  configuration shell (ici *.zshrc*)  : ```open ~/.zshrc```
Une fenêtre *.zshrc* s'ouvre. Descendre au niveau de la section *#Example aliases* et coller le path alias : ![image](https://user-images.githubusercontent.com/111517884/229460367-4777580b-c222-4c82-a295-0fa0f9f0e472.png)

Sauvegarder et fermer le fichier .zshrc.

- 4. Retour sur le terminal: entrer la commande suivante : ```source ~/.zshrc``` puis ```auth_app``` .
L'installation se fait, cela peut prendre quelques minutes : ![image](https://user-images.githubusercontent.com/111517884/229447768-f2bbf449-d8c1-418d-a15e-ceaaf5ce6d3e.png)
Une fois finie, l'application se lance directement.

### Lancement de l'application pré-installée : 

- 1. Ouvrir le terminal, entrer la commande suivante : ```auth_app```
L'application se lance automatiquement.

## Vue globale de l'interface utilisateur 

![image](https://user-images.githubusercontent.com/111517884/229437126-89ef3c13-1a24-4030-b06d-259dcb0e2141.png)

![image](https://user-images.githubusercontent.com/111517884/229435924-b7ca1c91-6d1a-4c1c-a454-8230a1c0d383.png)


 

## Un exemple d'utilisation pas à pas :

- 1. Entrer les données de l'auteur du dossier , de la victime (ou du témoin) et le numéro d’enquête dans la fenêtre qui s'ouvre au lancement de l'application. Cliquer sur "Validation" quand les données entrées sont complètes et correctes.
 ![image](https://user-images.githubusercontent.com/111517884/229438252-ae9e7e04-4907-48e4-bef0-3948ff90ea08.png)


- 2. Une nouvelle fenêtre s’ouvre avec 6 images proposées. Sélectionner entre une à cinq images qui ressemblent le plus à la personne recherchée, de la plus à la moins ressemblante. Une image sélectionnée sera encadrée d'un contour vert. Une fois le choix fini, cliquer sur le bouton "Next". De nouvelles images sont alors génerées à partir du choix précedent.
 
  ![image](https://user-images.githubusercontent.com/111517884/229438876-09cc8f9e-7807-4866-b8c3-efc14f6e1df4.png)

- 3. Si l’on s’est trompé dans notre choix d'images, ou qu'aucune des nouvelles images génerées ne nous satisfait, on peut revenir en arrière en cliquant sur une des cases de l’historique se situant à gauche. On peut revenir sur n'importe laquelle des génerations précedentes.

  ![image](https://user-images.githubusercontent.com/111517884/229450955-0d9fbc5f-953b-40a1-9b16-339777b6d7b4.png)



- 4. Une fois qu'une image correspond au portrait robot de la personne recherchée, sélectionner cette image (et seuleument celle-ci) et appuyer sur "Validation finale" : ![image](https://user-images.githubusercontent.com/111517884/229439954-3b0c155a-16b1-40c5-8feb-c9ebc1878cd7.png) .
Une fois que vous avez cliqué sur "Validation finale", aller jusqu'au bout du processus. Un retour en arrière génerera des bugs.


- 5. Entrer le nom et le path de votre fichier pdf. Il s’agit du rapport d’identification, retraçant le processus de création de votre portrait-robot.

  ![image](https://user-images.githubusercontent.com/111517884/229450713-6fbb5446-325a-4b6b-9276-560f4c592dcc.png)
  ![image](https://user-images.githubusercontent.com/111517884/229450753-e28022a2-61c2-43ce-800e-7580754c55de.png)


- 6. À la fin, le fichier obtenu ressemblera à celui-ci : 
  ![image](https://user-images.githubusercontent.com/111517884/229450867-ca879e13-43bf-4ff9-87af-8019e5729e08.png)

Le code QR renvoie vers le lien de la database utilisée.


## Options supplémentaires : 

Dans le dossier *Aut_app_group_zero* un fichier *out.log* est crée. Il retrace l'installation de l'application ainsi que l'exécution. Si un problème apparaît lors de l'utilisation, les codes erreur seront inscrits dans ce fichier. Veuillez nous envoyer ce fichier par mail pour que nous puissons corriger les erreurs.
  ![image](https://user-images.githubusercontent.com/111517884/229453407-7b105ca7-b4da-4487-9439-8b298c049eb7.png)

Quelques options sont modifiables : 
- Dans le dossier *Aut_app_group_zero* ouvrir le fichier *params.json* :
<img width="478" alt="image" src="https://user-images.githubusercontent.com/111517884/229455370-4cc2d278-2904-4269-9e8c-b9e2d4f911c1.png">
Vous pouvez alors modifier les paramètres de taille et de couleur (RBG =3, noir et blanc = 1 ) des images que vous utilisez.

- Dans le dossier *Aut_app_group_zero/Module* ouvrir le fichier *main.py*. Aux lignes 26, 27 et 28 vous pouvez : 
 - Activer le fun mode : ```fun = True```  # Fun mode
 - Créer un fichier .json à la fin de l'utilisation de l'application (comme le fichier .pdf mais sans les images) : ```json_make = True``` # Make a json recap
 - Désactiver le passage dans l'auto-encodeur des images ajoutées lors des nouvelles génerations : ```db_autocoded = False``` # Autoencode les images de la database

Une nouvelle version est en préparation, pour plus d'informations voir *Aut_app_group_zero/AE_OK_128.html* .




