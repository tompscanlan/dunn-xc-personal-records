import errno
import os
import re

import scrape
import pandas as pd
from dotenv import load_dotenv
from functools import lru_cache
import requests_cache
from bs4 import BeautifulSoup
import timeit

load_dotenv(verbose=True)  # take environment variables from .env.
RACES = [
    {
        "url": None,  # original data is in a pdf
        "path": "reservoir-park-invitational",
        "meet_name": "Reservoir Park Invitational 2021",
        "venue_name": 'Louisville, KY',
        "date": "Aug 14, 2021",
        "event_name": "Event 1 Girls 1 Mile Run CC K-1",
        "runners": 298,
        "dunn_runners": 298,
    },
    {
        "url": 'https://ky.milesplit.com/meets/436537-tully-invitational-2021/results/757560/raw',
        "meet_name": "Tully Invitational  2021",
        "venue_name": 'Charlie Vettiner Park',
        "date": "Aug 28, 2021",
        "path": "tully-invitational",
        "event_name": "Event 1 Girls 1 Mile Run CC K-1",
        "runners": 749
    },
    {
        "url": 'https://ky.milesplit.com/meets/436421-bluegrass-cross-country-invitational-2021/results/759967/raw',
        "meet_name": "Bluegrass Cross Country Invitational 2021",
        "venue_name": 'Masterson Station UK',
        "date": "Sep 4, 2021",
        "path": "bluegrass-cross-country-invitational",
        "event_name": None,
        "runners": 1420
    },
    {
        "url": 'https://ky.milesplit.com/meets/420062-rumble-through-the-jungle-2021/results/761414/raw',
        "path": "rumble-through-the-jungle",
        "meet_name": "Rumble Through the Jungle 2021",
        "venue_name": 'Creasey Mahan Nature Preserve',
        "date": "Sep 10, 2021                            Sep 11, 2021",
        "event_name": None,
        "runners": 867
    },
]

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

    if url is None:
        with open(filename, "r") as f:
            return f.read()
    else:
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


def line_to_runner(line: str) -> dict:
    return line


def get_runners(s: str) -> [dict]:
    runners: [dict] = []
    lines = re.split("\n|\r\n", s)

    for pattern in patterns:
        for i, line in enumerate(lines):
            match = pattern.match(line)
            if match is not None:
                group = match.groupdict()

                if group['athlete'] is None or str(group['athlete']).lower() == 'unknown':
                    print("failed to capture runner because of a bad name:" + group['athlete'])
                    continue

                runners.append(group)

            # for debugging failed matches
            # else:
            #     print(line)

            # if this is the last line, and we've matched at least once
            # then skip the next matchers
            if i == (len(lines)-1) and len(runners) > 0:
                break
        else:
            continue  # if loop didn't break, try next matcher
        break  # if inner did break, then skip remaining matchers

    return runners


def get_runners_dataframe(race: dict) -> (dict, pd.DataFrame):
    runners = get_milesplit_data(race['url'], race['meet_name'])
    runners = pd.DataFrame(data=get_runners(runners))

    # keep track of Dunn runners only
    runners = runners[runners['school'].astype('str').str.contains('Dunn')]
    # runners['year'] = pd.to_numeric(runners['year']).astype('int')


    # if this race has names formatted as "last, first" change it to 'first last'
    mixed_name = runners[runners['athlete'].str.match(r"\S+\s*,\s*\S+")]
    athletes = mixed_name['athlete'].str.split(r"\s*,\s*")
    mixed_name['athlete'] = [' '.join([i[1], i[0]]) for i in athletes]
    runners.update(mixed_name['athlete'])

    runners['athlete'] = runners['athlete'].str.lower()
    runners = runners.set_index(keys=['athlete']).sort_index()

    # Alterations, after original data creation
    if race['meet_name'] == "Reservoir Park Invitational 2021":
        # fix missed runner error:
        runners.loc['declan peek', 'time'] = '8:39.06'

    # turn string times into a time delta for use in comparisons
    runners = scrape.race_time_to_timedelta(runners, 'time', 'delta')

    # drop unneeded cols
    runners = runners.drop(columns=['school', 'time'])

    return runners


# debug regex https://regex101.com/r/eq8UqK/1
patternA = re.compile(r"""
^\s*
(?:\d+)
\s+
(?P<athlete>[\w.\s',-]+?(?<!\s))
\s+
(?P<year>(?:\d+|SO|FR|JR|SR|--|(?:M)\d|(?:W)\d)(?=\s))
\s+
(?:(?:\d+)\s+)?
(?P<school>[^\d]+(?<!\s))\s+(\d+)?
\s+
(?P<time>\d+:\d+.\d+)
\s+
(?:(?:\d+)\s+)?
([-\s\d.:]+)$
""", re.VERBOSE)

patternB = re.compile(r"""
^\s*
(?:\d+)
\s+
(?:#
(?:\d+)
)?
\s*
(?P<athlete>[\w\s,'-.]+?(?<!\s))
\s+
(?P<year>\d+)?
\s+
(?P<school>[\w\s.',-]+?(?<!\s))?
\s+
(?P<time>\d+:\d+.\d+)
\s+
(?:\d*)?
\s*
$
""", re.VERBOSE)

# for PDF format
patternC = re.compile(r"""
^\s*
(?:\d+)
\s+
(?P<athlete>[\w\s()'-.]+?)
\s
(?P<year>\d+)
\s
(?P<school>[\w.\s',-]+?(?<!\s))
\s*
(?P<time>\d+:\d+.\d+)
""", re.VERBOSE)

patterns = [patternA, patternB, patternC]


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

        # If the cache doesn't exist, pull the web page and cache it
        if not os.path.isfile(filename):
            runners = get_milesplit_data(race['url'], race['meet_name'])
            x = get_runners(runners)
            assert len(x) == race['runners']

            df = get_runners_dataframe(race)


            df.to_csv(filename)  # loses data types


if __name__ == "__main__":
    pull_data(RACES)
