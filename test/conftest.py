"""
datetime: Get the date for test date.
sys: For import `message` modules from `message/message`
pytest: For using fixture with pytest
"""

import datetime
import sys
import pytest
sys.path.append('.')

@pytest.fixture
def ohlcv_data():
    """
    Create OHLCV test data
    :return: hash
    """
    data = {
        'Date': '2020-12-29',
        'Open': '7620',
        'High': '8070',
        'Low': '7610',
        'Close': '8060',
        'Volume': '823700'
    }
    return data

@pytest.fixture
def prev_ohlcv_data():
    """
    Create yesterday OHLCV test data
    :return: hash
    """
    data = {
        'Date': '2020-12-28',
        'Open': '7500',
        'High': '8000',
        'Low': '7500',
        'Close': '8000',
        'Volume': '820000'
    }
    return data

@pytest.fixture
def today_datetime():
    """
    Today datetime
    :return: datetime
    """
    return datetime.date.today()
