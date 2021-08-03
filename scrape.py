import requests
from bs4 import BeautifulSoup
import re
import csv

csv_columns = ['index','bibnumber','name', 'year', 'school', 'time', 'points']

def write_csv(file, runners: [dict]):
    try:
        with open(file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in runners:
                writer.writerow(data)
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

    runner_line = re.compile("^\s*(?P<index>\d+)\s+#(?P<bibnumber>\d+)\s+(?P<name>[\w\s.',-]+)\s+(?P<year>\d+)\s+(?P<school>[\w\s.',-]+)\s+(?P<time>\d+:\d+.\d+)\s+(?P<points>\d*)\s+")
    for line in lines:
        match = runner_line.match(line)
        if (match != None):
            details = match.groupdict()
            details['name'] = details['name'].rstrip()
            details['school'] = details['school'].rstrip()
            runners.append(details)
        else:
            print("no match for: ", line)

    return runners

url = "https://ky.milesplit.com/meets/364782-ktccca-meet-of-champions-2019/results/676374/raw"
raw_results = get_raw_results(url)
