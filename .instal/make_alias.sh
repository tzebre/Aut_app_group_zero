echo "SCRIPT_DIR='$PWD'" > .instal/path.txt
echo "copy past : alias auth_app='source $PWD/execution.sh'"
cat .instal/path.txt .instal/execution_script.sh > execution.sh

