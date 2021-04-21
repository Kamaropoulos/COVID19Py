import pytest
from COVID19Py import COVID19


@pytest.fixture
def covid_obj():
    covid19 = COVID19()
    return covid19


def test_publisher_and_subscriber(covid_obj):
    save_curr_latestData = covid_obj.getAll()
    # After first invocation of getAll(), previousData should still be None
    assert covid_obj.previousDataObserver.previousData is None
    covid_obj.getAll()
    # After second invocation of getAll(), previousData should be equal to old latestData
    assert covid_obj.previousDataObserver.previousData is save_curr_latestData
