import scrape
import pandas as pd
import numpy as np

RACE_DATA_FILE = "2021_season_data/race_1"

BESTTIMES_FILE = "./2021_season_data/besttimes"
URL = 'https://ky.milesplit.com/meets/436537-tully-invitational-2021/results/757560/raw'
HTML_FILE = "./test_resources/436537-tully-invitational-2021.html"

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)

# Load current best times for all known runners
best_times = pd.read_pickle("%s.p" % BESTTIMES_FILE)
best_times.sort_index(inplace=True)

# parse new race data into a list of runners/times
page = scrape.get_race_from_url_or_html_file(URL, HTML_FILE)
raw_results = scrape.get_raw_results(page)
runners = scrape.get_runners(raw_results)

# this race, only Dunn runners, as a dataframe
tully = pd.DataFrame(data=runners)
tully = tully[tully['school'].astype('str').str.contains('Dunn')]
tully['year'] = pd.to_numeric(tully['year']).astype('int')

# turn string times into a time delta for use in comparisons
splittimes = tully['time'].str.split(r"[:.]", expand=True).astype(float)
tully['delta'] = pd.to_timedelta(splittimes[0], unit='m') + pd.to_timedelta(splittimes[1], unit='s') + pd.to_timedelta(splittimes[2] * 10, unit='ms')

# Tully race everyone ran 1 mile
tully['miles'] = 1
tully['mile_pace'] = tully['delta'] / tully['miles']

# this race has names formatted as "last, first", while best has "first last".
# compensate for that
tully[['lastname', 'firstname']] = tully.name.str.split(r"\s*,\s*", expand=True)
tully['name'] = [' '.join(i) for i in zip(tully["firstname"], tully["lastname"])]
tully['name'] = tully['name'].str.lower()
tully = tully.set_index(keys=['name'])
tully= tully.sort_index()

# drop unneeded cols
tully = tully.drop(columns=['index', 'bibnumber', 'points', 'lastname', 'firstname', 'school', 'time'])

# Store current race data
tully.to_csv("%s.csv" % RACE_DATA_FILE)  # loses data types
tully.to_pickle("%s.p" % RACE_DATA_FILE)  # preserves data types


# consolidate all best times and current race
all_runners = best_times.merge(tully, on='name', how='outer', indicator=True, suffixes=('_best', '_tully'))
# left_only means they missed this race but have run before
# right_only means this is their first race
# both means they ran before and in this race may have a PR

# capture runners that don't have an existing best time, add this pace to the best times
new_runners = pd.DataFrame()
new_runners = all_runners[ all_runners['_merge'] == "right_only"]
new_runners = new_runners.drop(columns=[ 'miles_best', 'mile_pace_best', 'year', '_merge', 'delta'])
new_runners = new_runners.rename(columns={'miles_tully': 'miles', 'mile_pace_tully': 'mile_pace'})
new_best = pd.DataFrame()
new_best = best_times.append(new_runners)

# times that improved, aka PRs
prs = pd.DataFrame()
prs = all_runners[ (all_runners['_merge'] == 'both') & (all_runners['mile_pace_best'] > all_runners['mile_pace_tully']) ]
prs['improvement'] = prs['mile_pace_best' ] - prs['mile_pace_tully']
prs.sort_values(by='improvement', inplace=True)
prs = prs.rename(columns={'miles_tully': 'miles', 'miles_best': 'miles_prior','mile_pace_best': 'mile_pace_prior', 'mile_pace_tully': 'mile_pace'})
prs = prs.drop(columns=['delta', 'year', '_merge'])
print("New PRs:")
print(prs)

# Store PRs for this race
prs.to_csv("%s.csv" % (RACE_DATA_FILE + "_prs"))  # loses data types
prs.to_pickle("%s.p" % (RACE_DATA_FILE + "_prs"))  # preserves data types

best_prs = prs.drop(columns=['improvement', 'miles_prior', 'mile_pace_prior'])
new_best.update(best_prs)

# Store latest best times
new_best.to_csv("%s.csv" % BESTTIMES_FILE)
new_best.to_pickle("%s.p" % BESTTIMES_FILE)