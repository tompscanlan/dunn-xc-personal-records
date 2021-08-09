#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import re
import csv
import sys
import sqlite3

DB_FILE = 'DXC-milesplit-data.db'
KM_PER_MILE = 1.609344

csv_columns = ['index','bibnumber','name', 'year', 'school', 'time', 'points']
runner_regexp = re.compile(r"^\s*(?P<index>\d+)\s+(?:#(?P<bibnumber>\d+)\s+)?(?P<name>[\w\s.',-]+)\s+(?P<year>\d*)\s+(?P<school>[\w\s.',-]+)\s+(?P<time>\d+:\d+.\d+)\s+(?P<points>\d*)\s+")
event_name_regexp = re.compile(r"^(?P<eventname>Event.*$)")


def read_csv(file):
    runners = []
    try:
        with open(file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=csv_columns)
            for row in reader:
                runners.append(row)
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(file, reader.line_num, e))

    return runners


def write_csv(file, runners: [dict]):
    try:
        with open(file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in runners:
                writer.writerow(data)
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(file, writer.line_num, e))


def write_raw(file: str, results: str):
    try:
        with open(file, 'w') as rawfile:
            count = rawfile.write(results)
            if count != len(results):
                print("error writing")
                exit(1)

    except IOError:
        print("I/O error")


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


def parse_url(url) -> str:
    page = requests.get(url)
    return page.content


def get_raw_results(page):
    soup = BeautifulSoup(page, "html.parser")
    results = soup.find(id="meetResultsBody")
    return results.text


def get_runners(s: str) -> [dict]:
    runners: [dict] = []
    lines = re.split("\n|\r\n", s)

    for line in lines:
        match = runner_regexp.match(line)
        if match is not None:
            details = match.groupdict()
            details['name'] = details['name'].rstrip()
            details['school'] = details['school'].rstrip()
            runners.append(details)
        # for debugging failed matches
        # else:
        #     print("no match for: ", line)
    return runners


def get_event_name(s: str) -> str:
    soup = BeautifulSoup(page, "html.parser")
    results = soup.find(id="meetResultsBody")

    lines = re.split("\n|\r\n", s)

    for line in lines:
        match = event_name_regexp.match(line)
        if match is not None:
            details = match.groupdict()
            if details['eventname'] is not None:
                return details['eventname'].rstrip()

def prep_db(connection):
    with connection:
        connection.execute(
            """
            CREATE TABLE MEETS (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
            )
            """
        )
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("must pass a url like "
              "'https://ky.milesplit.com/meets/364782-ktccca-meet-of-champions-2019/results/676374/raw'")
        exit(1)

    url = sys.argv[1]
    page = parse_url(url)
    raw_results = get_raw_results(page)
    runners = get_runners(raw_results)
    write_csv("results.csv", runners)

    connection = sqlite3.connect(DB_FILE)
    prep_db(connection)

