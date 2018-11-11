#!/bin/sh

BASEDIR=$(dirname "$0")
if [ "$#" -ne 1 ]
then
  echo -e "\033[1;34mUsage: gen-report.sh <eval.xls>\033[0m"
  exit 1
else
echo -e "\033[1;32m---------------------Generating Player Reports------------------------------\033[0m"
  TARGET=$1
  if [ -f $TARGET ]
  then
    echo -e "\033[1;32mProcessing [$TARGET].\033[0m"
    python $BASEDIR/evaluate.py $TARGET
  else
    echo -e "\033[1;35mFile [$TARGET] does not exist.\033[0m"
    exit 1
  fi
echo -e "\033[1;32m----------------------Player Reports Generation Complete-------------------------------\033[0m"
fi





