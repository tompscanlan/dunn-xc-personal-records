import scrape
import pandas as pd
import numpy as np


def sample_and_change_time(df: pd.DataFrame, n:int, seconds: int):
    sample = df.sample(n=n)

    # add seconds to our sample
    sample['deltas'] = sample['deltas'].apply(
        lambda x: x + pd.to_timedelta(pd.offsets.Second(seconds))
    )

    # update textual time with the new time
    sample['time'] = sample['deltas'].apply(
        lambda x: f'{x.components.minutes:d}:{x.components.seconds:02d}.{x.components.milliseconds/10:02.0f}' if not pd.isnull(x) else ''
    )

    df.update(sample)


file = "original/Reservoir Park Invitational 08-14-2021.txt"
textfile = open(file, 'r')
raw_results = textfile.read();

runners = scrape.get_runners(raw_results)

df = pd.DataFrame(data=runners)
times = df['time_pdf']
splittimes = times.str.split(r"[:.]", expand=True).astype(float)
deltas = pd.to_timedelta(splittimes[0], unit='m') + pd.to_timedelta(splittimes[1], unit='s') + pd.to_timedelta(splittimes[2]*10, unit='ms')
df['deltas'] = deltas
df['year'] = pd.to_numeric(df['year'])
df = df.drop(['index', 'bibnumber', 'name', 'year', 'school', 'time', 'points'], axis=1)
df = df.rename(columns={'name_pdf': "name", "year_pdf": "year", "team_pdf": "team", "time_pdf": "time"})

# loses data types
df.to_csv("2021_season_data/race_0.csv", index=False)
# preserves data types
df.to_pickle("2021_season_data/race_0.p")

de = pd.read_pickle("2021_season_data/race_0.p")
de.eq(df)

# test next race
r0 = pd.read_pickle("2021_season_data/race_0.p")
r1 = pd.read_pickle("2021_season_data/race_0.p")

sample_and_change_time(r1,5, -10)
sample_and_change_time(r1,5, 20)

pd.concat([r0,r1]).drop_duplicates(keep=False)

r1[r1['team'].isin(['Dunn'])]

runners = r1['name']
prs = r1[ r1['name', 'time']]
for i in r1.to_dict('r'):

pd.set_option('display.max_rows', None)
sorted = df.sort_values(by='deltas')
sorted = sorted[sorted['team'].astype('str').str.contains('Dunn')]
sorted[['name', 'year', 'time']]