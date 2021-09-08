#!/bin/bash

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
env
pyenv activate venv39
rm 2021_season_data/{besttimes,race_}*
python ./Reservoir_Park_Invitational.py
python ./tully_inviatational.py
python ./bluegrass_invitational.py