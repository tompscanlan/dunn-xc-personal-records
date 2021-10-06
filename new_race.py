import scrape
import pandas as pd
from dotenv import load_dotenv

scrape.pandas_set_big_print()

load_dotenv(verbose=True)  # take environment variables from .env.
race_url = 'https://ky.milesplit.com/meets/420062-rumble-through-the-jungle-2021/results/761414/raw'
race_short_name = '420062-rumble-through-the-jungle-2021'
race_number = 3

RACE_DATA_FILE = "{}/race_{}".format(scrape.SEASON_PATH, race_number)
HTML_FILE = "{}/{}.html".format(scrape.HTML_CACHE, race_short_name)

# Load current best times for all known runners
best_times = scrape.load_best_times()

# parse new race data from the web or a cache into a dataframe of runners and times
meet_details, runners = scrape.get_runners_dataframe(race_url, HTML_FILE)


# race everyone ran 2k
# km/m = d
# dm = km
runners['miles'] = 2 * scrape.MILE_PER_KM
runners['mile_pace'] = runners['delta'] / runners['miles']
runners = runners.drop(columns='delta')


# Store current race data
runners.to_csv("%s.csv" % RACE_DATA_FILE)  # loses data types
runners.to_pickle("%s.p" % RACE_DATA_FILE)  # preserves data types


# consolidate all best times and current race
all_runners = best_times.merge(runners, on='name', how='outer', indicator=True, suffixes=('_best', '_runners'))
# left_only means they missed this race but have run before, so don't update best time

# right_only means this is their first race
# capture runners that don't have an existing best time, add this pace to the best times
new_runners = all_runners[all_runners['_merge'] == "right_only"]
new_runners = new_runners.drop(columns=['miles_best', 'mile_pace_best', '_merge', 'year_best'])
new_runners = new_runners.rename(
    columns={'miles_runners': 'miles', 'mile_pace_runners': 'mile_pace', 'year_runners': 'year'})
new_best = best_times.append(new_runners)

# both means they ran before and in this race may have a PR
# times that improved, aka PRs
prs = all_runners[
    (all_runners['_merge'] == 'both') & (all_runners['mile_pace_best'] > all_runners['mile_pace_runners'])
]
prs['improvement'] = prs['mile_pace_best'] - prs['mile_pace_runners']

prs = prs.drop(columns=['year_best', '_merge'])
prs = prs.rename(columns={'miles_runners': 'miles', 'miles_best': 'miles_prior', 'mile_pace_best': 'mile_pace_prior',
                          'mile_pace_runners': 'mile_pace', 'year_runners': 'year'})
prs = prs.reset_index()
prs.sort_values(by='improvement', inplace=True)


# Store PRs for this race
prs.to_csv("%s.csv" % (RACE_DATA_FILE + "_prs"))  # loses data types
prs.to_pickle("%s.p" % (RACE_DATA_FILE + "_prs"))  # preserves data types

best_prs = prs.drop(columns=['improvement', 'miles_prior', 'mile_pace_prior'])
new_best.update(best_prs)

# make 9 and 6 groups of runners based on mile pace
new_best['groups-of-8'] = pd.qcut(new_best['mile_pace'], q=9, labels=False)
new_best['groups-of-12'] = pd.qcut(new_best['mile_pace'], q=6, labels=False)

# Store latest best times
new_best.to_csv("%s.csv" % scrape.BESTTIMES_FILE)
new_best.to_pickle("%s.p" % scrape.BESTTIMES_FILE)

new_best = new_best.reset_index()
new_best.sort_values(by='mile_pace', inplace=True)

scrape.send_pr_email(meet_details, prs, new_best)
