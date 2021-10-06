import scrape
import pandas as pd

RACE_DATA_FILE = "2021_season_data/race_2"
BESTTIMES_FILE = "./2021_season_data/besttimes"
URL = 'https://ky.milesplit.com/meets/436421-bluegrass-cross-country-invitational-2021/results/759967/raw'
HTML_FILE = "./test_resources/436421-bluegrass-cross-country-invitational-2021.html"

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)

# Load current best times for all known runners
best_times = scrape.load_best_times()

# parse new race data into a list of runners/times
# page = scrape.get_html_from_url_or_cache(URL, HTML_FILE)
# meet_details = scrape.get_meet_details(page)
# raw_results = scrape.get_milesplit_data(page)

# parse new race data from the web or a cache into a dataframe of runners and times
meet_details, bluegrass = scrape.get_runners_dataframe(URL, HTML_FILE)

# runners = scrape.get_runners(raw_results)


# this race, only Dunn runners, as a dataframe
# bluegrass = pd.DataFrame(data=runners)
# bluegrass = bluegrass[bluegrass['school'].astype('str').str.contains('Dunn')]
# bluegrass['year'] = pd.to_numeric(bluegrass['year']).astype('int')

# turn string times into a time delta for use in comparisons
# bluegrass = scrape.race_time_to_timedelta(bluegrass, 'time', 'delta')

# Tully race everyone ran 1 mile
# km/m = d
# dm = km
bluegrass['miles'] = 2 * scrape.MILE_PER_KM
bluegrass['mile_pace'] = bluegrass['delta'] / bluegrass['miles']
bluegrass = bluegrass.drop(columns='delta')

# this race has names formatted as "last, first", while best has "first last".
# compensate for that
# bluegrass[['lastname', 'firstname']] = bluegrass.name.str.split(r"\s*,\s*", expand=True)
# bluegrass['name'] = [' '.join(i) for i in zip(bluegrass["firstname"], bluegrass["lastname"])]
# bluegrass['name'] = bluegrass['name'].str.lower()
# bluegrass = bluegrass.set_index(keys=['name'])
# bluegrass= bluegrass.sort_index()

# drop unneeded cols
# bluegrass = bluegrass.drop(columns=['index', 'bibnumber', 'points', 'lastname', 'firstname', 'school', 'time', 'delta'])

# Store current race data
bluegrass.to_csv("%s.csv" % RACE_DATA_FILE)  # loses data types
bluegrass.to_pickle("%s.p" % RACE_DATA_FILE)  # preserves data types


# consolidate all best times and current race
all_runners = best_times.merge(bluegrass, on='name', how='outer', indicator=True, suffixes=('_best', '_bluegrass'))
# left_only means they missed this race but have run before
# right_only means this is their first race
# both means they ran before and in this race may have a PR

# capture runners that don't have an existing best time, add this pace to the best times
new_runners = pd.DataFrame()
new_runners = all_runners[ all_runners['_merge'] == "right_only"]
new_runners = new_runners.drop(columns=[ 'miles_best', 'mile_pace_best', '_merge', 'year_best'])
new_runners = new_runners.rename(columns={'miles_bluegrass': 'miles', 'mile_pace_bluegrass': 'mile_pace', 'year_bluegrass': 'year'})
new_best = pd.DataFrame()
new_best = best_times.append(new_runners)

# times that improved, aka PRs
prs = pd.DataFrame()
prs = all_runners[ (all_runners['_merge'] == 'both') & (all_runners['mile_pace_best'] > all_runners['mile_pace_bluegrass']) ]
prs['improvement'] = prs['mile_pace_best' ] - prs['mile_pace_bluegrass']

prs = prs.drop(columns=['year_best', '_merge'])
prs = prs.rename(columns={'miles_bluegrass': 'miles', 'miles_best': 'miles_prior','mile_pace_best': 'mile_pace_prior',
                          'mile_pace_bluegrass': 'mile_pace', 'year_bluegrass': 'year'})
prs['year'] = pd.to_numeric(prs['year']).astype('int')
prs = prs.reset_index()
prs.sort_values(by='improvement', inplace=True)

# scrape.send_pr_email(meet_details,prs)

# Store PRs for this race
prs.to_csv("%s.csv" % (RACE_DATA_FILE + "_prs"))  # loses data types
prs.to_pickle("%s.p" % (RACE_DATA_FILE + "_prs"))  # preserves data types

best_prs = prs.drop(columns=['improvement', 'miles_prior', 'mile_pace_prior'])
new_best.update(best_prs)

# make 9 and 6 groups of runners based on mile pace
new_best['groups-of-8'] = pd.qcut(new_best['mile_pace'], q=9, labels=False)
new_best['groups-of-12'] = pd.qcut(new_best['mile_pace'], q=6, labels=False)

# Store latest best times
new_best.to_csv("%s.csv" % BESTTIMES_FILE)
new_best.to_pickle("%s.p" % BESTTIMES_FILE)