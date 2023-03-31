SCRIPT=$(readlink -f "$_")
SCRIPT_DIR=$(dirname "$SCRIPT")
conda > /dev/null
if [ $? -ne 0 ]; then
    Distrib=$uname
    if [ $expr $Distrib = 'Darwin' ]; then
        curl "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh" -o SCRIPT_DIR/Miniconda3-latest-MacOSX-x86_64.sh
        bash SCRIPT_DIR/Miniconda3-latest-MacOSX-x86_64.sh
        chemin=$(whereis conda | awk '{print $2}')
        $chemin init
        conda  > /dev/null
    else
        curl "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" -o SCRIPT_DIR/Miniconda3-latest-Linux-x86_64.sh
        bash SCRIPT_DIR/Miniconda3-latest-Linux-x86_64.sh
        chemin=$(whereis conda | awk '{print $2}')
        $chemin init
        conda > /dev/null
    fi
    if [ $? -eq 0 ]; then
        echo "Conda a été installé avec succès"
    else
        echo "Conda n'a pas pu être installé"
        exit 1
    fi
else
    echo "Conda est déjà installé"
fi
conda info --envs | grep "Enviro_group_zero" > /dev/null
if [ $? -eq 0 ]; then
    echo "Environnement déjà présent"
    conda activate Enviro_group_zero
    conda list > $SCRIPT_DIR/.comp_tmp.txt
    pip list > $SCRIPT_DIR/.pip_tmp.txt
    cmp $SCRIPT_DIR/.comp_tmp.txt $SCRIPT_DIR/.env.txt
    if [ $? -eq 0 ]; then
        echo "L'environnement est correctement chargé"
    else
        echo "L'environnement n'est pas correctement chargé"
        conda activate base
        conda remove -n Enviro_group_zero --all
    fi
    cmp $SCRIPT_DIR/.comp_tmp.txt S$CRIPT_DIR/.pip_env.txt
    if [ $? -eq 0 ]; then
        echo "L'environnement est correctement chargé"
    else
        echo "L'environnement n'est pas correctement chargé"
        pip install -r $SCRIPT_DIR/requirement.txt
    fi
fi
conda info --envs | grep "Enviro_group_zero" > /dev/null
if [ $? -ne 0 ]; then
    conda env create -f env.yml
    if [ $? -eq 0 ]; then
        echo "L'environnement a été créé succès"
        conda activate Enviro_group_zero
        conda list > $SCRIPT_DIR/.env.txt
        pip list > $SCRIPT_DIR/.pip_env.txt
    else
        echo "L'environnement n'a pas été créé"
        exit 1
    fi
fi

rm $SCRIPT_DIR/.comp_tmp.txt
cd $SCRIPT_DIR/Module
python3 main.py
cd -


