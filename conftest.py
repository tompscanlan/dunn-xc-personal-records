import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--runnetwork", action="store_true", default=False, help="run tests that hit the network"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runnetwork"):
        # --runnetwork given in cli: do not skip slow tests
        return
    skip_network = pytest.mark.skip(reason="need --runnetwork option to run")
    for item in items:
        if "network" in item.keywords:
            item.add_marker(skip_network)