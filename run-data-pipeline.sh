#!/bin/bash

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
env
pyenv activate venv39
rm 2021_season_data/besttimes.*
rm "2021_season_data/"*"-prs.csv"

rm "2021_season_data/csv/Bluegrass Cross Country Invitational 2021.csv"
rm "2021_season_data/csv/Gatorland 2021.csv"
rm "2021_season_data/csv/Reservoir Park Invitational 2021.csv"
rm "2021_season_data/csv/Rumble Through the Jungle 2021.csv"
rm "2021_season_data/csv/Tully Invitational  2021.csv"

python ./pull_data.py
python ./best_times_all_races.py

#
#python ./Reservoir_Park_Invitational.py  # 0
#python ./tully_inviatational.py  # 1
#python ./bluegrass_invitational.py  # 2
#python ./new_race.py 'https://ky.milesplit.com/meets/420062-rumble-through-the-jungle-2021/results/761414/raw' \
#                     '420062-rumble-through-the-jungle-2021' 3
#
#race_url = 'https://ky.milesplit.com/meets/436561-gatorland-2021/results/764160/raw'
#race_short_name = '436561-gatorland-2021'
#race_number = 4
#
#race_url = 'https://ky.milesplit.com/meets/436561-gatorland-2021/results/764164/raw'
#race_short_name = '436561-gatorland-2021'
#race_number = 4