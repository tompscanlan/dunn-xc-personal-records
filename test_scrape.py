import os
import pytest
import scrape

scrapes = [
    {
        "url": "https://ky.milesplit.com/meets/364782-ktccca-meet-of-champions-2019/results/676374/raw",
        "path": "test_resources/364782-ktccca-meet-of-champions-2019",
        "runners": 374
    },
    {
        "url": "https://ky.milesplit.com/meets/341354-tiger-run-2019/results/660303/raw",
        "path": "test_resources/341354-tiger-run-2019",
        "runners": 332
    },
    {
        "url": "https://ky.milesplit.com/meets/361881-madisonville-classic-2019/results/660850/raw",
        "path": "test_resources/361881-madisonville-classic-2019-660850",
        "runners": 77
    },
    {
        "url": "https://ky.milesplit.com/meets/361881-madisonville-classic-2019/results/660851/raw",
        "path": "test_resources/361881-madisonville-classic-2019-660851",
        "runners": 48
    },


]

def test_get_runners():
    for s in scrapes:
        raw_file = s["path"] + ".raw"

        assert os.path.exists(raw_file), raw_file + " should exist, may need to run with --runnetwork first"
        with open(raw_file, 'r') as file:
            raw_scrape = file.read()

        assert raw_scrape is not None
        assert "Name" in raw_scrape
        assert "Event" in raw_scrape

        runners = scrape.get_runners(raw_scrape)
        assert isinstance(runners, list)
        assert len(runners) == s["runners"]


@pytest.mark.network
def test_scrape():
    for s in scrapes:
        results = scrape.get_raw_results(s["url"])

        assert results is not None
        assert "Name" in results
        assert "Event" in results

        runners = scrape.get_runners(results)
        assert len(runners) == s["runners"]

        scrape.write_csv(s["path"] + ".csv", runners)
        scrape.write_raw(s["path"] + ".raw", results)


def test_csv_reader():
    for s in scrapes:
        runners = scrape.read_csv(s["path"] + ".csv")
        assert len(runners) == s["runners"] +1

