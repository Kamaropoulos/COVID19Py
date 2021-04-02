import pytest
from COVID19Py.covid19 import COVID19


@pytest.fixture
def first_instance():
    """
    :return: an instance of the COVID19 class
    """
    return COVID19()


@pytest.fixture
def second_instance():
    """
    :return: an instance of the COVID19 class
    """
    return COVID19()


def test_singleton_pattern(first_instance, second_instance):
    """
    Test to check if the instances are equal; they must be equal for Singleton Pattern to have been correctly applied.

    :param first_instance: an instance of COVID19
    :param second_instance: another instance of COVID19
    :return: bool: returns the boolean value for the equality of the instances
    """
    assert first_instance is second_instance
