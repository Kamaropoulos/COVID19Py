from COVID19Py import COVID19, DataFetcher
import pytest


@pytest.fixture
def interface_obj():
    covid19 = COVID19()
    abs_interface = DataFetcher(covid19)
    return abs_interface


def test_getAll(interface_obj):
    try:
        interface_obj.getAll()
    except Exception as err:
        assert False


def test_getLatestChanges(interface_obj):
    try:
        interface_obj.getLatestChanges()
    except Exception as err:
        assert False


def test_getLatest(interface_obj):
    try:
        interface_obj.getLatest()
    except Exception as err:
        assert False

def test_getLocations(interface_obj):
    try:
        interface_obj.getLocations()
    except Exception as err:
        assert  False

def test_getLocationByCountryCode(interface_obj):
    try:
        interface_obj.getLocationByCountryCode("CA")
    except Exception as err:
        assert False

def test_getLocationByCountry(interface_obj):
    try:
        interface_obj.getLocationByCountry("Canada")
    except Exception as err:
        assert False

def test_getLocationById(interface_obj):
    try:
        interface_obj.getLocationById(1)
    except Exception as err:
        assert False





