import scrape
import pandas as pd
import dotenv
import os

dotenv.load_dotenv(verbose=True)
password = os.environ.get('SENDER_PASSWORD')
sender_email = os.environ.get('SENDER_EMAIL')
receiver_email = os.environ.get('TO_EMAIL').split(",|,\s+")
print ("to {}, from {}, pass '{}'".format(receiver_email, sender_email, password))

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
(meet_details, tully) = scrape.get_runners_dataframe(URL, HTML_FILE)

# Tully race everyone ran 1 mile
tully['miles'] = 1
tully['mile_pace'] = tully['delta'] / tully['miles']
tully = tully.drop(columns='delta')

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
new_runners = new_runners.drop(columns=['miles_best', 'year_best', 'mile_pace_best', '_merge'])
new_runners = new_runners.rename(columns={'miles_tully': 'miles', 'mile_pace_tully': 'mile_pace', 'year_tully': 'year'})
new_best = pd.DataFrame()
new_best = best_times.append(new_runners)

# times that improved, aka PRs
prs = pd.DataFrame()
prs = all_runners[ (all_runners['_merge'] == 'both') & (all_runners['mile_pace_best'] > all_runners['mile_pace_tully']) ]
prs['improvement'] = prs['mile_pace_best' ] - prs['mile_pace_tully']
prs.sort_values(by='improvement', inplace=True)
prs = prs.rename(columns={'year_tully': 'year', 'miles_tully': 'miles', 'miles_best': 'miles_prior','mile_pace_best': 'mile_pace_prior', 'mile_pace_tully': 'mile_pace'})
prs = prs.drop(columns=['year_best', '_merge'])
prs['year'] = pd.to_numeric(prs['year']).astype('int')
prs = prs.reset_index()
prs.sort_values(by='improvement', inplace=True)

# scrape.send_pr_email(meet_details,prs)

# make 9 and 6 groups of runners based on mile pace
new_best['groups-of-8'] = pd.qcut(new_best['mile_pace'], q=9, labels=False)
new_best['groups-of-12'] = pd.qcut(new_best['mile_pace'], q=6, labels=False)

# Store PRs for this race
prs.to_csv("%s.csv" % (RACE_DATA_FILE + "_prs"))  # loses data types
prs.to_pickle("%s.p" % (RACE_DATA_FILE + "_prs"))  # preserves data types

best_prs = prs.drop(columns=['improvement', 'miles_prior', 'mile_pace_prior'])
new_best.update(best_prs)

# Store latest best times
new_best.to_csv("%s.csv" % BESTTIMES_FILE)
new_best.to_pickle("%s.p" % BESTTIMES_FILE)