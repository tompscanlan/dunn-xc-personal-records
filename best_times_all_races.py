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


def calculate_best_times(races: [dict], func) -> [pd.DataFrame]:
    df_list = []
    best_times = pd.DataFrame()

    for i, race in enumerate(races):
        print("Calculating race #{} for {}".format(i, race['meet_name'], race['url']))
        cvs_cache_file = "{}/{}.csv".format(scrape.CSV_CACHE, race['meet_name'])
        pr_file = "{}/{}.csv".format(scrape.PRS_CACHE, race['meet_name'])

        # If the csv cache doesn't exist, fail
        if not os.path.isfile(cvs_cache_file):
            print("{} ought to exist but doesn't!".format(cvs_cache_file))
            print("might need to run pull_data.py")
            exit(5)

        current_race = pd.read_csv(cvs_cache_file)
        current_race = current_race.set_index(keys=['athlete']).sort_index()
        current_race['mile_pace'] = pd.to_timedelta(current_race['mile_pace'])
        current_race = func(current_race)
        df_list.append(current_race)

        # load current best time data
        best_times = scrape.load_best_times()

        # consolidate all best times and current race
        all_runners = best_times.merge(current_race, on='athlete', how='outer', indicator=True,
                                       suffixes=('_best', '_current'))
        # left_only means they missed this race but have run before, so don't update best time

        # right_only means this is their first race
        # capture runners that don't have an existing best time, add this pace to the best times
        first_time_runner = all_runners[all_runners['_merge'] == "right_only"]
        first_time_runner = first_time_runner.drop(columns=['miles_best', 'mile_pace_best', 'time_best', '_merge', 'year_best'], errors='ignore')
        first_time_runner = first_time_runner.rename(
            columns={'miles_current': 'miles', 'mile_pace_current': 'mile_pace', 'year_current': 'year', 'time_current': 'time'})
        # append because they don't exist in the existing best times list
        best_times = best_times.append(first_time_runner)

        # both means they ran before and in this race may have a PR
        # times that improved, aka PRs
        prs = all_runners[
            (all_runners['_merge'] == 'both') & (all_runners['mile_pace_best'] >= all_runners['mile_pace_current'])
            ].copy()
        prs['improvement'] = prs['mile_pace_best'] - prs['mile_pace_current']

        # child's grade leve doesn't matter in best time calculation
        prs = prs.drop(columns=['year_best', '_merge'])
        prs = prs.rename(
            columns={'time_best': 'time_prior', 'miles_best': 'miles_prior', 'mile_pace_best': 'mile_pace_prior',
                     'year_current': 'year', 'time_current': 'time', 'miles_current': 'miles',
                     'mile_pace_current': 'mile_pace'})
        # prs = prs.reset_index()
        prs.sort_values(by='improvement', inplace=True)
        # Store PRs for this race
        scrape.df_to_csv(prs, pr_file)

        best_prs = prs.drop(columns=['improvement', 'miles_prior', 'mile_pace_prior'])
        best_times.update(best_prs)

        best_times_grouped = best_times.copy()
        # make 9 and 6 groups of runners based on mile pace
        best_times_grouped['groups-of-8'] = pd.qcut(best_times_grouped['mile_pace'], q=9, labels=False, duplicates='drop')
        best_times_grouped['groups-of-12'] = pd.qcut(best_times_grouped['mile_pace'], q=6, labels=False, duplicates='drop')
        # Store latest best times
        scrape.store_best_times(best_times_grouped)

    return df_list


if __name__ == "__main__":
    # df1 = calculate_best_times(scrape.RACES, keep_above_one_mile)
    df2 = calculate_best_times(scrape.RACES, keep_only_2k)

    exit(0)
