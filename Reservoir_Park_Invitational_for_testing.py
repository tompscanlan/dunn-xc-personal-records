import scrape
import pandas as pd
import numpy as np


def sample_and_change_time(df: pd.DataFrame, n:int, seconds: int):
    sample = df.sample(n=n)

    # add seconds to our sample
    sample['delta'] = sample['delta'].apply(
        lambda x: x + pd.to_timedelta(pd.offsets.Second(seconds))
    )

    # update textual time with the new time
    sample['time'] = sample['delta'].apply(
        lambda x: f'{x.components.minutes:d}:{x.components.seconds:02d}.{x.components.milliseconds/10:02.0f}' if not pd.isnull(x) else ''
    )

    df.update(sample)


file = "original/Reservoir Park Invitational 08-14-2021.txt"
textfile = open(file, 'r')
raw_results = textfile.read()

runners = scrape.get_runners(raw_results)

df = pd.DataFrame(data=runners)
times = df['time_pdf']
splittimes = times.str.split(r"[:.]", expand=True).astype(float)
delta = pd.to_timedelta(splittimes[0], unit='m') + pd.to_timedelta(splittimes[1], unit='s') + pd.to_timedelta(splittimes[2]*10, unit='ms')
df['delta'] = delta
df = df.drop(['index', 'bibnumber', 'name', 'year', 'school', 'time', 'points'], axis=1)
df = df.rename(columns={'name_pdf': "name", "year_pdf": "year", "team_pdf": "team", "time_pdf": "time"})
df['year'] = pd.to_numeric(df['year'])

halfmile = df[ (df['delta'] < pd.to_timedelta(10, unit='m')) &  (df['year'] < 2)]

df['miles'] = 1
halfmile['miles'] = 0.5
df.update(halfmile)

# loses data types
df.to_csv("2021_season_data/race_0.csv", index=False)
# preserves data types
df.to_pickle("2021_season_data/race_0.p")

df['mile_pace'] = df['delta'] * 1/df['miles']
df['best_mile_time'] = df['mile_pace']
best = df[['name', 'team', 'year', 'best_mile_time']]
best = best.sort_values(by='best_mile_time')
best.to_csv("2021_season_data/besttimes.csv")
best.to_pickle("2021_season_data/besttimes.p")

# test next race
r0 = pd.read_pickle("2021_season_data/race_0.p")
r1 = pd.read_pickle("2021_season_data/race_0.p")

sample_and_change_time(r1,5, -10)
sample_and_change_time(r1,5, 20)

#pd.concat([r0,r1]).drop_duplicates(keep=False)

r0 = r0[r0['team'].astype('str').str.contains('Dunn')]
r1 = r1[r1['team'].astype('str').str.contains('Dunn')]

# r1[r1['team'].isin(['Dunn'])]

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)

sorted = df.sort_values(by='delta')
sorted = sorted[sorted['team'].astype('str').str.contains('Dunn')]
sorted[['name', 'year', 'time']]

both = pd.merge(left=r0, right=r1, left_on='name', right_on='name')
prs = both[both['delta_x'] > both['delta_y']]
prs['improvement'] = prs['delta_x'] - prs['delta_y']

prs = prs.sort_values(by='improvement')
prs[['name', 'delta_x', 'delta_y', 'improvement']]

record = prs[['name','delta_y']]
record.rename(columns={'delta_y': 'besttime'})
record.to_csv('besttimes.csv')
record.to_pickle('besttimes.p')