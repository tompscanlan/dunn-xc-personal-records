import os
import pytest
import scrape
import pandas as pd


scrapes = [
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
        "runners": 48
    },
]

def test_get_runners():
    for s in scrapes:
        raw_html = s["path"] + ".html"

        assert os.path.exists(raw_html), raw_html + " should exist, may need to run with --runnetwork first"
        with open(raw_html, 'r') as file:
            raw_html = file.read()

        assert "html" in raw_html, "raw_html doesn't look like html"
        raw_results = scrape.get_raw_results(raw_html)

        assert raw_results is not None, "raw_results should be set"
        assert "Name" in raw_results, "raw_results must content Name"
        assert "Event" in raw_results, "raw_results must content Event"

        runners = scrape.get_runners(raw_results)
        assert runners is not None, "runners should be set"
        assert isinstance(runners, list), "runners should be a list"
        assert len(runners) == s["runners"], "incorrect runners count"
        for r in runners:
            assert r["time"] is not None, "time shouldn't be empty for runner " + r["name"]
            assert len(r["name"]) <25

        meet_details = scrape.get_meet_details(raw_html)
        assert meet_details['meet_name'] == s['meet_name']
        assert meet_details['venue_name'] == s['venue_name']
        assert meet_details['date'] == s['date']


@pytest.mark.network
def test_scrape():
    for s in scrapes:

        page = scrape.parse_url(s["url"])
        with open(s["path"] + ".html", "w") as f:
            f.write(page)

        results = scrape.get_raw_results(page)

        assert results is not None
        assert "Name" in results
        assert "Event" in results

        runners = scrape.get_runners(results)
        assert len(runners) == s["runners"]

        event_name = scrape.get_event_name(results)
        meet_details = scrape.get_meet_details(page)

        for r in runners:
            r.update(meet_details)
            r.update(event_name)

        df = pd.DataFrame(data=runners)
        df.to_csv("./data/" + meet_details['meet_name'] + '-' + event_name['eventname'] + '.csv')
