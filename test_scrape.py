import os
import pytest
import scrape
import pandas as pd


scrapes = [
    {
        "url": 'https://ky.milesplit.com/meets/436421-bluegrass-cross-country-invitational-2021/results/759967/raw',
        "meet_name": "Bluegrass Cross Country Invitational 2021",
        "venue_name": 'Masterson Station UK',
        "date": "Sep 4, 2021",
        "path": "test_resources/436421-bluegrass-cross-country-invitational-2021",
        "event_name": None,
        "runners": 1420
    },
    {
        "url": None,
        "meet_name": "Reservoir Park Invitational 2021",
        "venue_name": 'Louisville, KY',
        "date": "Aug 14, 2021",
        "path": "test_resources/reservior-park-invitational-2021",
        "event_name": "Event 1 Girls 1 Mile Run CC K-1",
        "runners": 298
    },
    {
        "url": 'https://ky.milesplit.com/meets/436537-tully-invitational-2021/results/757560/raw',
        "meet_name": "Tully Invitational  2021",
        "venue_name": 'Charlie Vettiner Park',
        "date": "Aug 28, 2021",
        "path": "test_resources/436537-tully-invitational-2021",
        "event_name": "Event 1 Girls 1 Mile Run CC K-1",
        "runners": 749
    },
    {
        "url": "https://ky.milesplit.com/meets/364782-ktccca-meet-of-champions-2019/results/676374/raw",
        "meet_name": "KTCCCA Meet of Champions 2019",
        "venue_name": 'Masterson Station Park',
        "date": "Oct 19, 2019",
        "path": "test_resources/364782-ktccca-meet-of-champions-2019",
        "event_name": "Event 4  Boys 2000 Meter Run CC 4th & Under",
        "runners": 374
    },
    {
        "url": "https://ky.milesplit.com/meets/341354-tiger-run-2019/results/660303/raw",
        'meet_name': 'Tiger Run 2019',
        'venue_name': 'Louisville Champions Park',
        'date': 'Aug 24, 2019',
        "path": "test_resources/341354-tiger-run-2019",
        "event_name": "Event 2  Boys 3k Run CC Middle Schoo Middle School",
        "runners": 332
    },
    {
        "url": "https://ky.milesplit.com/meets/361881-madisonville-classic-2019/results/660850/raw",
        "meet_name": "Madisonville Classic 2019",
        "venue_name": 'Madisonville North Hopkins High School',
        "date": "Aug 24, 2019",
        "path": "test_resources/361881-madisonville-classic-2019-660850",
        "event_name": "Event 5  Boys 1600 Meter Run CC",
        "runners": 77
    },
    {
        "url": "https://ky.milesplit.com/meets/361881-madisonville-classic-2019/results/660851/raw",
        'meet_name': 'Madisonville Classic 2019',
        'venue_name': 'Madisonville North Hopkins High School',
        'date': 'Aug 24, 2019',
        "path": "test_resources/361881-madisonville-classic-2019-660851",
        "event_name": "Event 6  Girls 1600 Meter Run CC",
        "runners": 46  # actually 48 with two set to 'Unknown' names
    },
]


def load_raw_from_html_file(path: str) -> str:
    html_path = path + ".html"

    assert os.path.exists(html_path), html_path + " should exist, may need to run with --runnetwork first"
    with open(html_path, 'r') as file:
        raw_html = file.read()

    return raw_html


def test_get_runners():
    for s in scrapes:

        raw_html = load_raw_from_html_file(s["path"])
        assert "html" in raw_html, "raw_html doesn't look like html"

        raw_results = scrape.get_raw_results(raw_html)
        assert raw_results is not None, "raw_results should be set"
        # assert "Name" in raw_results, "raw_results must content Name"
        # assert "Event" in raw_results, "raw_results must content Event"

        meet_details = scrape.get_meet_details(raw_html)
        assert meet_details['meet_name'] == s['meet_name']
        assert meet_details['venue_name'] == s['venue_name']
        assert meet_details['date'] == s['date']

        runners = scrape.get_runners(raw_results)
        assert runners is not None, "runners should be set"
        assert isinstance(runners, list), "runners should be a list"
        assert len(runners) == s["runners"], "incorrect runners count"
        for r in runners:
            assert r["time"] is not None, "time shouldn't be empty for runner " + r["name"]
            assert r["name"] is not None, "name shouldn't be empty for runner " + meet_details['meet_name'] + r
            assert len(r["name"]) < 25, "name should be less than 25 chars for runner " + r["name"]
            assert r['school'] is not None, "school should not be empty for runner " + r["name"]
            assert not str(r['school']).endswith(" "), "school should not end with space for runner " + r["name"]



def test_runners_dataframe():
    for s in scrapes:
        raw_html = load_raw_from_html_file(s["path"])
        raw_results = scrape.get_raw_results(raw_html)
        runners = scrape.get_runners(raw_results)

        df = pd.DataFrame(data=runners)
        assert None not in df['name']
        assert None not in df['school']
        assert None not in df['time']
        assert None not in df['year']

        times = df['time']
        splittimes = times.str.split(r"[:.]", expand=True).astype(float)
        delta = pd.to_timedelta(splittimes[0], unit='m') + pd.to_timedelta(splittimes[1], unit='s') + pd.to_timedelta(splittimes[2]*10, unit='ms')
        assert None not in delta



@pytest.mark.network
def test_scrape():
    for s in scrapes:

        if None == s['url']:
            continue

        page = scrape.parse_url(s["url"])
        results = scrape.get_raw_results(page)

        assert results is not None
        assert "Name" in results
        assert "Event" in results

        runners = scrape.get_runners(results)
        assert len(runners) == s["runners"]

        with open(s["path"] + ".html", "w") as f:
            f.write(page)
