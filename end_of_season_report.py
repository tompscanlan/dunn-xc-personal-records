import os

import pandas as pd
import scrape


def keep_above_one_mile(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['miles'] >= 1]


def keep_2k(df: pd.DataFrame) -> pd.DataFrame:
     x = df[df['miles'] >= 2 * scrape.MILE_PER_KM]
     return x


def keep_only_2k(df: pd.DataFrame) -> pd.DataFrame:
    df['miles'] = df['miles'].astype('float')
    x = df[(df['miles'] >= 2 * scrape.MILE_PER_KM) &
           (df['miles'] < 3 * scrape.MILE_PER_KM)]
    return x


def gather_all_times(races: [dict]) -> [pd.DataFrame]:
    df_list = []
    runners = pd.DataFrame()

    for i, race in enumerate(races):
        print("Calculating race #{} for {}".format(i, race['meet_name'], race['url']))
        cvs_cache_file = "{}/{}.csv".format(scrape.CSV_CACHE, race['meet_name'])

        # If the csv cache doesn't exist, fail
        if not os.path.isfile(cvs_cache_file):
            print("{} ought to exist but doesn't!".format(cvs_cache_file))
            print("might need to run pull_data.py")
            exit(5)

        current_race = pd.read_csv(cvs_cache_file)
        # current_race = current_race.set_index(keys=['athlete']).sort_index()
        cr = current_race[['athlete', 'time']].copy()
        cr['race'] = race['meet_name']
        runners = runners.append(cr)

    return runners


if __name__ == "__main__":
    runners = gather_all_times(scrape.RACES)
    # df2 = gather_all_times(scrape.RACES, keep_only_2k)
    p = runners.pivot(index=['athlete'], columns=['race'], values=['time'])
    p.to_csv('all.csv')
    exit(0)
