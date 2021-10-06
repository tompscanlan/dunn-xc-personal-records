#!/bin/bash

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
env
pyenv activate venv39
rm 2021_season_data/{besttimes,race_}*
python ./pull_data.py

python ./Reservoir_Park_Invitational.py  # 0
python ./tully_inviatational.py  # 1
python ./bluegrass_invitational.py  # 2
python ./new_race.py 'https://ky.milesplit.com/meets/420062-rumble-through-the-jungle-2021/results/761414/raw' \
                     '420062-rumble-through-the-jungle-2021' 3