#/bin/bash

# Always use most up-to-date stable build on master branch
git fetch all;
git reset --hard origin/master;

mode=$1
if [[ $mode == "dev" ]]; then # For Developer Mode
  python RUNME.py | tee today.log
elif [[ $mode == "team" ]]; then # For Team (Real Run)
  #statements
  python RUNME.py team | tee today.log
else # Assume Developer Mode
  python RUNME.py | tee today.log
fi
