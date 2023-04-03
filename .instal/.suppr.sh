conda activate base
conda info --envs | grep "Enviro_group_zero" >/dev/null
if [ $? -eq 0 ]; then
    conda remove -n Enviro_group_zero --all
    if [ $? -eq 0 ]; then
        echo "L'environnement a été supprimé avec succès !"
    else
        echo "L'environnement n'a pas pu être surpprimé "
    fi
else
    echo "L'environnement n'existe déjà plus"
fi
echo "Veuillez supprimer l'alias auth_app dans votre fichier config"
