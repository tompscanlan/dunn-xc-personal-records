#!/bin/bash

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
env
pyenv activate venv39
rm 2021_season_data/besttimes.*

rm "2021_season_data/csv/Bluegrass Cross Country Invitational 2021.csv"
rm "2021_season_data/csv/Gatorland 2021.csv"
rm "2021_season_data/csv/Reservoir Park Invitational 2021.csv"
rm "2021_season_data/csv/Rumble Through the Jungle 2021.csv"
rm "2021_season_data/csv/Tully Invitational  2021.csv"
rm "2021_season_data/csv/Haunted Woods Classic 2021.csv"
rm "2021_season_data/csv/Bates 2021.csv"


python ./pull_data.py
python ./best_times_all_races.py
