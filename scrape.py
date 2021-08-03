#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import re
import csv
import sys

csv_columns = ['index','bibnumber','name', 'year', 'school', 'time', 'points']
runner_regexp = re.compile(r"^\s*(?P<index>\d+)\s+(?:#(?P<bibnumber>\d+)\s+)?(?P<name>[\w\s.',-]+)\s+(?P<year>\d*)\s+(?P<school>[\w\s.',-]+)\s+(?P<time>\d+:\d+.\d+)\s+(?P<points>\d*)\s+")

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
            if (count != len(results)):
                print("error writing")
                exit(1)

    except IOError:
        print("I/O error")

def get_raw_results(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="meetResultsBody")

    return re.sub("\r\n", "\n", results.text)

def get_runners(s: str) -> [dict]:
    runners: [dict] = []
    lines = re.split("\n|\r\n", s)

    for line in lines:
        match = runner_regexp.match(line)
        if (match != None):
            details = match.groupdict()
            details['name'] = details['name'].rstrip()
            details['school'] = details['school'].rstrip()
            runners.append(details)
        # for debugging failed matches
        # else:
        #     print("no match for: ", line)

    return runners

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("must pass a url like 'https://ky.milesplit.com/meets/364782-ktccca-meet-of-champions-2019/results/676374/raw'")
        exit(1)

    url = sys.argv[1]
    raw_results = get_raw_results(url)
    runners = get_runners(raw_results)
    write_csv("results.csv", runners)
