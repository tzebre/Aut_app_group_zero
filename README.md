# info_7
Authors :
- BACQUIE Camille 
- DUVERT Quentin
- LETHULLIER Lea
- OHAYON Quentin @Quentinohn
- MATHIEU Théo @tzebre

Exporter un environnement Conda
```
	conda env export > environment.yml
```
 	 
Supression de l'environnement et re-creation de l'environnement
```
	conda remove -n soft_dev
	conda env create -n soft_dev -f environment.yml
```
 Activation 
```
	conda activate soft_dev
```