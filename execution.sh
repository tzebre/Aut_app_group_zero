conda > /dev/null
if [ $? -ne 0 ]; then
    Distrib=$uname
    if [ $expr $Distrib='Darwin' ]; then
        curl "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh" -o Miniconda3-latest-MacOSX-x86_64.sh
        bash Miniconda3-latest-MacOSX-x86_64.sh
        conda  > /dev/null
    else
        curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
        bash Miniconda3-latest-Linux-x86_64.sh
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
    conda list > .comp_tmp.txt
    cmp .comp_tmp.txt .env.txt
    if [ $? -eq 0 ]; then
        echo "L'environnement est correctement chargé"
    else
        echo "L'environnement n'est pas correctement chargé"
        conda activate base
        conda remove -n Enviro_group_zero --all
    fi
fi
conda info --envs | grep "Enviro_group_zero" > /dev/null
if [ $? -ne 0 ]; then
    conda env create -n Enviro_group_zero  --file env.yml
    if [ $? -eq 0 ]; then
        echo "L'environnement a été créé succès"
        conda activate Enviro_group_zero
        conda list > .env.txt
    else
        echo "L'environnement n'a pas été créé"
        exit 1
    fi
fi

rm .comp_tmp.txt
cd app
python3 autentificator.py
cd ..
