#!/usr/bin/env python
import errno

import requests_cache
from functools import lru_cache
from bs4 import BeautifulSoup
import re
import csv
import sys
import pandas as pd
import os.path
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table
import dotenv
import os
import hashlib

dotenv.load_dotenv(verbose=True)
# email setup
port = 465  # For SSL
password = os.environ.get('SENDER_PASSWORD')
sender_email = os.environ.get('SENDER_EMAIL')
receiver_email = os.environ.get('TO_EMAIL').split(",|,\s+")
smtp_server = "smtp.gmail.com"
print ("to {}, from {}, pass '{}'".format(receiver_email, sender_email, password))
# Create a secure SSL context
context = ssl.create_default_context()

requests_session = requests_cache.CachedSession('dunnxc_cache', backend='filesystem', serializer='yaml', expire_after=None)

RACE_SEASON = 2021
SEASON_PATH = "{}_season_data".format(RACE_SEASON)
BESTTIMES_FILE = "{}/besttimes".format(SEASON_PATH)
CACHE_PATH = "./{}".format(SEASON_PATH)
CSV_CACHE = "{}/csv".format(CACHE_PATH)
HTML_CACHE = "{}/html".format(CACHE_PATH)
TEXT_CACHE = "{}/text".format(CACHE_PATH)

DB_FILE = 'DXC-milesplit-data.db'
KM_PER_MILE = 1.609344
MILE_PER_KM = 1/KM_PER_MILE


RACES = [
    {
        # this race needed to fix declan peek's 'time' to '8:39.06'
        # also fix Orla's name to "Dunne Gillies, Orla"
        "url": None,  # original data is in a pdf
        "path": "reservoir-park-invitational",
        "meet_name": "Reservoir Park Invitational 2021",
        "venue_name": 'Louisville, KY',
        "date": "Aug 14, 2021",
        "event_name": "Event 1 Girls 1 Mile Run CC K-1",
        "runners": 298,
        "dunn_runners": 64,

    },
    {
        "url": 'https://ky.milesplit.com/meets/436537-tully-invitational-2021/results/757560/raw',
        "meet_name": "Tully Invitational  2021",
        "venue_name": 'Charlie Vettiner Park',
        "date": "Aug 28, 2021",
        "path": "tully-invitational",
        "event_name": "Event 1 Girls 1 Mile Run CC K-1",
        "runners": 749,
        "dunn_runners": 45,
    },
    {
        "url": 'https://ky.milesplit.com/meets/436421-bluegrass-cross-country-invitational-2021/results/759967/raw',
        "meet_name": "Bluegrass Cross Country Invitational 2021",
        "venue_name": 'Masterson Station UK',
        "date": "Sep 4, 2021",
        "path": "bluegrass-cross-country-invitational",
        "event_name": None,
        "runners": 1420,
        "dunn_runners": 30,
    },
    {
        "url": 'https://ky.milesplit.com/meets/420062-rumble-through-the-jungle-2021/results/761414/raw',
        "path": "rumble-through-the-jungle",
        "meet_name": "Rumble Through the Jungle 2021",
        "venue_name": 'Creasey Mahan Nature Preserve',
        "date": "Sep 10, 2021                            Sep 11, 2021",
        "event_name": None,
        "runners": 867,
        "dunn_runners": 54,
    },
    {
        "url": None,  # original data is split across two urls
        "path": "gatorland",
        "meet_name": "Gatorland 2021",
        "venue_name": 'Bowling Green, KY',
        "date": "Sep 17, 2021",
        "runners": 215,
        "dunn_runners": 27,
    },

]

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

PATTERNS = [patternA, patternB, patternC]

event_name_regexp = re.compile(r"^(?P<eventname>Event.*$)")


def pandas_set_big_print():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 200)

# Store latest best times
def store_best_times(df: pd.DataFrame):
        x = df.reset_index()
        x.to_pickle("{}.p".format(BESTTIMES_FILE))
        x.to_csv("{}.csv".format(BESTTIMES_FILE))

def load_best_times() -> pd.DataFrame:
    filename = "{}.p".format(BESTTIMES_FILE)

    # If it exists, load current best times for all known runners
    if os.path.isfile(filename):
        best_times = pd.read_pickle("{}.p".format(BESTTIMES_FILE))
        best_times.sort_index(inplace=True)
    else:
        best_times = pd.DataFrame()
        best_times['athlete'] = None
        best_times['year'] = None
        best_times['miles'] = None
        best_times['mile_pace'] = None


    best_times['athlete'] = best_times['athlete'].str.lower()
    best_times = best_times.set_index(keys=['athlete']).sort_index()
    return best_times


def get_meet_details(page) -> dict:
    details = {}
    soup = BeautifulSoup(page, "html.parser")
    details['meet_name'] = soup.select_one(".meetName").text
    details['meet_name'] = re.sub("\n|\r\n", "", details['meet_name'])
    details['meet_name'] = details['meet_name'].rstrip()
    details['meet_name'] = details['meet_name'].lstrip()

    details['venue_name'] = soup.select_one(".venueName").text
    details['venue_name'] = re.sub("\n|\r\n", "", details['venue_name'])

    details['date'] = soup.select_one(".date").text
    details['date'] = re.sub("\n|\r\n", "", details['date'])
    details['date'] = details['date'].rstrip()
    details['date'] = details['date'].lstrip()

    return details


# this is cached behind the scenes
def parse_url(url: str) -> str:
    r = requests_session.get(url)
    return r.text


@lru_cache(maxsize=32)
def get_raw_results(url: str):
    page_contents = parse_url(url)
    soup = BeautifulSoup(page_contents, "html.parser")
    results = soup.find(id="meetResultsBody")
    return results.text


def get_event_name(s: str) -> str:
    soup = BeautifulSoup(s, "html.parser")
    results = soup.find(id="meetResultsBody")

    lines = re.split("\n|\r\n", s)

    for line in lines:
        match = event_name_regexp.match(line)
        if match is not None:
            details = match.groupdict()
            if details['eventname'] is not None:
                details['eventname'].rstrip()
                return details


def get_html_from_url_or_cache(url: str, file: str) -> str:
    page = ""

    # create dirs for the cache, if needed
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # If the cache doesn't exist, pull the web page and cache it
    if not os.path.isfile(file):
        page = parse_url(url)
        with open(file, "w") as f:
            f.write(page)

    # otherwise, read from cache
    else:
        with open(file, "r") as f:
            page = f.read()

    return page


def race_time_to_timedelta(d: pd.DataFrame, timecol: str, deltacol: str) -> (dict, pd.DataFrame):
    splittimes = d[timecol].str.split(r"[:.]", expand=True).astype(float)
    d[deltacol] = pd.to_timedelta(splittimes[0], unit='m') + pd.to_timedelta(splittimes[1], unit='s') + \
                  pd.to_timedelta(splittimes[2] * 10, unit='ms')
    return d


def get_runners_dataframe(url: str, html_file: str) -> (dict, pd.DataFrame):

    page = get_html_from_url_or_cache(url, html_file)
    details = get_meet_details(page)
    results = get_raw_results(page)
    # print(results)
    runners = pd.DataFrame(data=get_runners(results))

    # keep track of Dunn runners only
    runners = runners[runners['school'].astype('str').str.contains('Dunn')]
    # runners['year'] = pd.to_numeric(runners['year']).astype('int')

    # turn string times into a time delta for use in comparisons
    runners = race_time_to_timedelta(runners, 'time', 'delta')

    # if this race has names formatted as "last, first" change it to 'first last'
    mixed_name = runners[runners['name'].str.match(r"\S+\s*,\s*\S+")]
    names = mixed_name['name'].str.split(r"\s*,\s*")
    mixed_name['name'] = [' '.join([i[1], i[0]]) for i in names]
    runners.update(mixed_name['name'])

    runners['name'] = runners['name'].str.lower()
    runners = runners.set_index(keys=['name']).sort_index()

    # drop unneeded cols
    runners = runners.drop(columns=['index', 'bibnumber', 'points', 'school', 'time'])

    return details, runners


def runners_df(url: str, cache_name: str) -> (dict, pd.DataFrame):

    if cache_name is None:
        cache_name = hashlib.sha256(url)

    page = get_html_from_url_or_cache(url, cache_name)
    details = get_meet_details(page)
    results = get_raw_results(page)
    # print(results)
    runners = pd.DataFrame(data=get_runners(results))

    # keep track of Dunn runners only
    runners = runners[runners['school'].astype('str').str.contains('Dunn')]
    # runners['year'] = pd.to_numeric(runners['year']).astype('int')

    # turn string times into a time delta for use in comparisons
    runners = race_time_to_timedelta(runners, 'time', 'delta')

    # if this race has names formatted as "last, first" change it to 'first last'
    mixed_name = runners[runners['name'].str.match(r"\S+\s*,\s*\S+")]
    names = mixed_name['name'].str.split(r"\s*,\s*")
    mixed_name['name'] = [' '.join([i[1], i[0]]) for i in names]
    runners.update(mixed_name['name'])

    runners['name'] = runners['name'].str.lower()
    runners = runners.set_index(keys=['name']).sort_index()

    # drop unneeded cols
    runners = runners.drop(columns=['index', 'bibnumber', 'points', 'school', 'time'])

    return details, runners



def send_pr_email(details, df, best):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg['Subject'] = f'PRs for {details["meet_name"]}'
    body = ("""
PRs for {} on {}:

{}

---------
Best overall mile times:
{}
""".format(details['meet_name'], details['date'], build_table(
        df[['athlete', 'year', 'mile_pace_prior', 'mile_pace', 'improvement']], 'red_light'),
           build_table(
               best, 'red_light')
           ))
    msg.attach(MIMEText(body, "html"))
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)


def find_prs(races: [dict]):

    for i, race in enumerate(races):
        best = load_best_times()

        print("Checking PRs for race #{} for {}".format(i, race['meet_name'], race['url']))
        filename = "{}/{}.csv".format(CSV_CACHE, race['meet_name'])
        prs_filename = "{}/{}-prs.csv".format(CACHE_PATH, race['meet_name'])


        # If the cache doesn't exist, there's a problem, should have run pull_data
        assert True == os.path.isfile(filename)

        # read in race data, and make mile pace a time delta
        runners = pd.read_csv(filename, parse_dates=True)
        runners['athlete'] = runners['athlete'].str.lower()
        runners = runners.set_index(keys=['athlete']).sort_index()
        runners['mile_pace'] = pd.to_timedelta(runners['mile_pace'])

        # should be a fixed number of runners for each specific race
        assert len(runners) == race['dunn_runners'], "runners len: {} is not {}".format(len(runners), race['dunn_runners'])

        # consolidate all best times and current race
        # left_only means they missed this race but have run before
        all_runners = best.merge(runners, on='athlete', how='outer', indicator=True, suffixes=('_best', '_current'))

        # capture new runners that don't have an existing best time
        # and add this pace to the best times.
        # right_only means this is their first race
        new_runners = pd.DataFrame()
        new_runners = all_runners[ all_runners['_merge'] == "right_only"]
        new_runners = new_runners.drop(columns=['miles_best', 'mile_pace_best', '_merge', 'year_best', 'groups-of-8', 'groups-of-12'], errors='ignore')
        new_runners = new_runners.rename(columns={'miles_current': 'miles',
                                                  'mile_pace_current': 'mile_pace',
                                                  'year_current': 'year'})

        # --------------
        prs = pd.DataFrame()

        # runners that were in besttimes and in current race
        # where current race time is less than prior best time, aka PRs.
        # both means they ran before and in this race may have a PR
        prs = all_runners[ (all_runners['_merge'] == 'both')
                           & (all_runners['mile_pace_best'] > all_runners['mile_pace_current'])]
        prs['improvement'] = prs['mile_pace_best' ] - prs['mile_pace_current']

        # clean up columns created in the merge
        prs = prs.drop(columns=['year_best', '_merge', 'groups-of-8', 'groups-of-12'], errors='ignore')
        prs = prs.rename(columns={'miles_current': 'miles',
                                  'miles_best': 'miles_prior',
                                  'mile_pace_best': 'mile_pace_prior',
                                  'mile_pace_current': 'mile_pace',
                                  'year_current': 'year'})
        # prs['year'] = pd.to_numeric(prs['year']).astype('int')


        prs.sort_values(by='improvement', inplace=True)
        prs = prs.loc[ prs['miles'] >= 1 ]
        # Store PRs for this race


        new_best = pd.DataFrame()
        new_best = best.append(new_runners)
        new_best.update(prs)
        # make 9 and 6 groups of runners based on mile pace
        new_best['groups-of-8'] = pd.qcut(new_best['mile_pace'], q=9, labels=False)
        new_best['groups-of-12'] = pd.qcut(new_best['mile_pace'], q=6, labels=False)
        # don't store best times below a mile race
        new_best = new_best.loc[ new_best['miles'] >= 1 ]

        # Store latest best times, and PRs
        store_best_times(new_best)
        prs = prs.reset_index()
        prs.to_csv(prs_filename)

        # --------------

    new_best = new_best.reset_index()
    new_best.sort_values(by='mile_pace', inplace=True)
    send_pr_email(race, prs, new_best)


if __name__ == "__main__":

    find_prs(RACES)