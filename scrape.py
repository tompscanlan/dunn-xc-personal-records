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

csv_columns = ['index', 'bibnumber', 'name', 'year', 'school', 'time', 'points']

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


def load_best_times() -> pd.DataFrame:
    # Load current best times for all known runners
    best_times = pd.read_pickle("%s.p" % BESTTIMES_FILE)
    best_times.sort_index(inplace=True)
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
        df[['name', 'year', 'mile_pace_prior', 'mile_pace', 'improvement']], 'red_light'),
           build_table(
               best, 'red_light')
           ))
    msg.attach(MIMEText(body, "html"))
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("must pass a url like "
              "'https://ky.milesplit.com/meets/364782-ktccca-meet-of-champions-2019/results/676374/raw'")
        exit(1)

    url = sys.argv[1]
    page = parse_url(url)
    raw_results = get_raw_results(page)
    runners = get_runners(raw_results)
    event_name = get_event_name(raw_results)
    meet_details = get_meet_details(page)

    for r in runners:
        r.update(meet_details)
        r.update(event_name)

    df = pd.DataFrame(data=runners)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = pd.to_numeric(df['year']).astype('int')

    df.to_csv("./data/" + meet_details['meet_name'] + '.csv', index=False)