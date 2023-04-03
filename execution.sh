#SCRIPT=$(readlink -f "$_")
#SCRIPT_DIR=$(dirname "$SCRIPT")
#replace by path
#alias app_auth="source PATH/info_7/execution.sh"
SCRIPT_DIR="/Users/theomathieu/Documents/cours/4A/S2/dev_log/code/info_7"
SE_=$(cat $SCRIPT_DIR/.ASCII.txt)
printf ${SE_}
CPU=$(sysctl -n machdep.cpu.brand_string)
MEMORY=$(sysctl -n hw.memsize)
Os_=$(uname)
Dir_=${SCRIPT_DIR}
Date_=$(date +'%Y-%m-%d %H:%M:%S')
echo -e "$(date +'%Y-%m-%d\t%H:%M:%S')" > $SCRIPT_DIR/out.log
echo "App directory: ${SCRIPT_DIR}" >> $SCRIPT_DIR/out.log
echo "Operating System: $(sw_vers -productName)" >> $SCRIPT_DIR/out.log
echo "Version System: $(sw_vers -productVersion)" >> $SCRIPT_DIR/out.log
echo "CPU: $CPU" >> $SCRIPT_DIR/out.log
echo "Memory: $MEMORY" >> $SCRIPT_DIR/out.log

Error_txt="Erreur lors du lancement de l'Application.\n Merci d'envoyer le rapport de log à support@group_zero.com \n Path du rapport :  ${SCRIPT_DIR}/out.log"
echo ${NE_}
echo  "Group_zero à votre service 🫡"
printf "\e[0m Start Authetificator App: \e[1;32m%s\e[0m\n" "$Date_"
printf "\e[0m Directory of App: \e[1;32m%s\e[0m\n" "$Dir_"
printf "\e[0m Your OS is: \e[1;32m%s\e[0m\n" "$Os_"

conda >/dev/null
printf "\e[0m Initialisation de conda: ... 🐍\e[0m\n"
if [ $? -ne 0 ]; then
  if [[ $(uname) == "Darwin" ]]; then
    curl "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh" -o $SCRIPT_DIR/Miniconda3-latest-MacOSX-x86_64.sh | tee -a $SCRIPT_DIR/out.log
    bash $SCRIPT_DIR/Miniconda3-latest-MacOSX-x86_64.sh
    chemin=$(whereis conda | awk '{print $2}')
    $chemin init
    conda >/dev/null
  else
    curl "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" -o $SCRIPT_DIR/Miniconda3-latest-Linux-x86_64.sh | tee -a $SCRIPT_DIR/out.log
    bash $SCRIPT_DIR/Miniconda3-latest-Linux-x86_64.sh
    chemin=$(whereis conda | awk '{print $2}')
    $chemin init
    conda >/dev/null
  fi
  if [ $? -eq 0 ]; then
    echo "Conda a été installé avec succès" >> $SCRIPT_DIR/out.log
    printf "\e[0m Instalation de conda:\e[1;32m Réussi \e[0m👍\n"
  else
    echo "Conda n'a pas pu être installé" >> $SCRIPT_DIR/out.log
    printf "\e[0m Instalation de conda:\e[1;31m Echec \e[0m😢\n"
    printf ${Error_txt}
    exit 1
  fi
else
  echo "Conda est déjà installé" >> $SCRIPT_DIR/out.log
  printf "\e[0m Conda:\e[1;32m Déjà installé \e[0m😁\n"
fi
if [[ $(uname) == "Darwin" ]]; then
  env="env.yml"
else
  env="env_linux.yml"
fi
conda info --envs | grep "Enviro_group_zero" >/dev/null
if [ $? -eq 0 ]; then
  echo "Environnement déjà présent" >> $SCRIPT_DIR/out.log
  printf "\e[0m Enviro_group_zero:\e[1;32m Déjà installé \e[0m👍\n"
  conda activate Enviro_group_zero
  conda list >$SCRIPT_DIR/.comp_tmp.txt
  cmp $SCRIPT_DIR/.comp_tmp.txt $SCRIPT_DIR/.env.txt
  if [ $? -eq 0 ]; then
    echo "L'environnement est correctement chargé" >> $SCRIPT_DIR/out.log
    printf "\e[0m Enviro_group_zero:\e[1;32m Complet \e[0m✅\n"
  else
    echo "L'environnement n'est pas correctement chargé" >> $SCRIPT_DIR/out.log
    printf "\e[0m Enviro_group_zero:\e[1;31m Erroné \e[0m⛔️\n"
    conda activate base
    conda remove -n Enviro_group_zero --all
    printf "\e[0m Enviro_group_zero:\e[1;38;5;208m Supprimé \e[0m🗑️️\n"
  fi
fi
conda info --envs | grep "Enviro_group_zero" >/dev/null
if [ $? -ne 0 ]; then
  echo "Creation de l'environement python 🐍⚒️"
  conda env create -f $SCRIPT_DIR/$env | tee -a $SCRIPT_DIR/out.log #tej les print degeux de la console
  conda info --envs | grep "Enviro_group_zero" >/dev/null
  if [ $? -eq 0 ]; then
    echo "L'environnement a été créé succès" >> $SCRIPT_DIR/out.log
    printf "\e[0m Enviro_group_zero:\e[1;32m Creé \e[0m⚒️️️\n"
    conda activate Enviro_group_zero
    conda list >$SCRIPT_DIR/.env.txt
    conda list >$SCRIPT_DIR/.comp_tmp.txt
  else
    echo "L'environnement n'a pas été créé" >> $SCRIPT_DIR/out.log
    printf "\e[0m Enviro_group_zero:\e[1;31m Echec de la creation \e[0m😢\n"
    printf ${Error_txt}
    exit 0 #fin de merde faut que ca cut le script
  fi
fi

rm $SCRIPT_DIR/.comp_tmp.txt
cd $SCRIPT_DIR/Module
echo "##Execution de l'app##" >> $SCRIPT_DIR/out.log
printf "Execution du code Python ... 🐍\n"
python3 main.py >> $SCRIPT_DIR/out.log
# shellcheck disable=SC2164
cd -
printf "Merci d'avoir utilisé AUTHETIFICATOR à bientot.\nGroup_zero à votre service 🫡\n"