import scrape
import pandas as pd

SEASON_DATA = "2021_season_data"
RACE_DATA = "%s/race_0" % SEASON_DATA
DATA_BESTTIMES = "%s/besttimes" % SEASON_DATA

URL = ''
HTML_FILE = "./test_resources/reservior-park-invitational-2021.html"

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)

page = scrape.get_html_from_url_or_cache(URL, HTML_FILE)
raw_results = scrape.get_raw_results(page)
runners = scrape.get_runners(raw_results)

df = pd.DataFrame(data=runners)
df['name'] = df['name'].str.lower()
df = df.set_index(keys=['name'])
df = df.sort_index()

df = df.drop(['index', 'bibnumber', 'points'], axis=1)
df = df[df['school'].astype('str').str.contains('Dunn')]

# fix missed runner error:
df.loc['declan peek', 'time'] = '8:39.06'

# what year are these folks?
df['year'] = pd.to_numeric(df['year']).astype('int')
print("folks with a grade less than 1: is this a problem?")
print(df[df['year'] < 1])

df = scrape.race_time_to_timedelta(df, 'time', 'delta')

# everyone ran a mile
df['miles'] = 1
# except those under year 2 ran a half mile
halfmile = df.copy()
halfmile = halfmile[ (halfmile['delta'] < pd.to_timedelta(10, unit='m')) &  (halfmile['year'] < 2)]
halfmile['miles'] = 0.5
df.update(halfmile)

# remove less than mile runners
df = df[ df['miles'] >= 1]

df['mile_pace'] = df['delta'] / df['miles']
df = df.drop(columns='delta')

df.sort_values(by='mile_pace', inplace=True)
best = df.copy()
best = best.drop(columns=['school', 'time'])
print(best)
best.to_csv("%s.csv" % DATA_BESTTIMES)
best.to_pickle("%s.p" % DATA_BESTTIMES)

df = df.drop(columns=['school', 'time'])
df.sort_index(inplace=True)
# loses data types
df.to_csv("%s.csv" % RACE_DATA)
# preserves data types
df.to_pickle("%s.p" % RACE_DATA)