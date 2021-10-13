import errno
import os
import pandas as pd
from dotenv import load_dotenv
from functools import lru_cache
import requests_cache
from bs4 import BeautifulSoup
import scrape

load_dotenv(verbose=True)  # take environment variables from .env.

requests_session = requests_cache.CachedSession('dunnxc_cache', backend='filesystem', expire_after=None)


# this is cached behind the scenes
def parse_url(url: str) -> str:
    r = requests_session.get(url)
    return r.text


# get the milesplit textual data from a URL, caching the result for future use
# also, if there is no URL, try reading from a text file named after the race name.
@lru_cache(maxsize=32)
def get_milesplit_data(url: str, file: str) -> str:
    filename = "{}/{}.txt".format(scrape.TEXT_CACHE, file)

    # try cache first
    if os.path.isfile(filename):
        print("Cache hit for {}".format(filename))
        with open(filename, "r") as f:
            return f.read()

    # otherwise
    if url is None:
        if not os.path.isfile(filename):
            print("Cache file {} doesn't exist, and we have no URL to pull from")
            exit(5)

        print("Cache hit for manually created data file {}".format(filename))

        with open(filename, "r") as f:
            return f.read()
    else:
        print("Creating cache for {}")
        page_contents = parse_url(url)
        soup = BeautifulSoup(page_contents, "html.parser")
        results = soup.find(id="meetResultsBody")
        with open(filename, "w") as f:
            f.write(results.text)

        return results.text


def get_html(url: str) -> str:
    page = parse_url(url)
    return page


def rename_key(d: dict, frm: str, to: str) -> dict:
    if frm in d:
        if d[frm] is not None:
            d[to] = d[frm]

        d.pop(frm, None)

    return d


def get_runners_dataframe(race: dict) -> (dict, pd.DataFrame):
    runners_text = get_milesplit_data(race['url'], race['meet_name'])
    runners = pd.DataFrame(data=scrape.get_runners(runners_text, race['pattern']))

    assert len(runners.index) == race['runners'], "{}: {} is not {}, as expected".format(race['meet_name'],
                                                                                         len(runners.index),
                                                                                         race['runners'])
    # keep track of Dunn runners only
    runners = runners[runners['school'].astype('str').str.contains('Dunn')]
    # runners['year'] = pd.to_numeric(runners['year']).astype('int')

    # if this race has names formatted as "last, first" change it to 'first last'
    mixed_name = runners[runners['athlete'].str.match(r"\S+\s*,\s*\S+")]
    athletes = mixed_name['athlete'].str.split(r"\s*,\s*")
    mixed_name['athlete'] = [' '.join([i[1], i[0]]) for i in athletes]
    runners.update(mixed_name['athlete'])

    # Alterations, after original data creation
    if race['meet_name'] == "Reservoir Park Invitational 2021":
        # fix missed runner error:
        declan = runners.loc[runners['athlete'] == 'Declan Peek']
        declan['time'] = '8:39.06'
        runners.update(declan)

        seb = runners.loc[runners['athlete'] == 'Sebastiano Bianconcin']
        seb['athlete'] = 'Sebastiano Bianconcini'
        runners.update(seb)

        # everyone ran a mile
        runners['miles'] = 1
        # except those under year 2 ran a half mile
        halfmile = runners.copy()
        halfmile = halfmile[halfmile['year'].astype(int) < 2]
        halfmile['miles'] = 0.5
        runners.update(halfmile)

    elif race['meet_name'] == "Tully Invitational  2021":
        # Tully race everyone ran 1 mile
        runners['miles'] = 1

    elif race['meet_name'] == "Bluegrass Cross Country Invitational 2021":
        runners['miles'] = 2 * scrape.MILE_PER_KM
    elif race['meet_name'] == "Rumble Through the Jungle 2021":
        runners['miles'] = 2 * scrape.MILE_PER_KM
    elif race['meet_name'] == "Gatorland 2021":
        runners['miles'] = 2 * scrape.MILE_PER_KM
    elif race['meet_name'] == "8th Annual S.I.C Invitational 2021":
        # Use year to signify K distance
        runners['miles'] = runners['year'].astype('int') * scrape.MILE_PER_KM
    elif race['meet_name'] == 'Bates 2021':
        runners['miles'] = 1

    elif race['meet_name'] == 'Haunted Woods Classic 2021':
        # Set everyone as a 3k
        runners['miles'] = 3 * scrape.MILE_PER_KM

        # younger kids did a 2k
        younger = runners[runners['year'].astype(int) < 4]
        younger['miles'] = 2 * scrape.MILE_PER_KM
        runners.update(younger)


    # turn string times into a time delta for use in comparisons
    runners = scrape.race_time_to_timedelta(runners, 'time', 'delta')
    runners['mile_pace'] = runners['delta'] / runners['miles']

    runners['athlete'] = runners['athlete'].str.lower()
    runners = runners.set_index(keys=['athlete']).sort_index()

    # drop unneeded cols
    runners = runners.drop(columns=['school', 'delta'])

    return runners


def pull_data(races: [dict]):
    for i, race in enumerate(races):
        print("Getting race #{} for {}".format(i, race['meet_name'], race['url']))
        filename = "{}/{}.csv".format(scrape.CSV_CACHE, race['meet_name'])

        # create dirs for the cache, if needed
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # If the csv cache doesn't exist, pull the web page and cache it
        if not os.path.isfile(filename):
            # runners = get_milesplit_data(race['url'], race['meet_name'])
            # x = scrape.get_runners(runners)
            # assert len(x) == race['runners'], "{} is not {}, as expected".format(len(x), race['runners'])

            df = get_runners_dataframe(race)
            assert len(df.index) == race['dunn_runners'], "{}: {} is not {}, as expected".format(
                race['meet_name'], len(df.index), race['dunn_runners'])
            df.to_csv(filename)


if __name__ == "__main__":
    pull_data(scrape.RACES)
