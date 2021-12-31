"""
ohlcv: Test target class
"""

from message import ohlcv

def test__compared_numbers_previous_day(ohlcv_data, prev_ohlcv_data):
    """
    Test method for `Ohlcv().__compared_numbers_previous_day`
    :param ohlcv: OHLCV data of stock price
    :type: hash
    :param prev_ohlcv: OHLCV data of stock price of yesterday
    :type: hash
    :return: Result assertion
    """
    compared_data = ohlcv.Ohlcv(ohlcv_data, prev_ohlcv_data).compared_numbers_previous_day
    expected_data = dict(
        Open='△120',
        High='△70',
        Low='△110',
        Close='△60',
        Volume='△3,700'
    )
    assert compared_data == expected_data
    
def test___compared_percent_previous_day(ohlcv_data, prev_ohlcv_data):
    """
    Test method for `Ohlcv().__compared_percent_previous_day`
    :param ohlcv: OHLCV data of stock price
    :type: hash
    :param prev_ohlcv: OHLCV data of stock price of yesterday
    :type: hash
    :return: Result assertion
    """
    compared_data = ohlcv.Ohlcv(ohlcv_data, prev_ohlcv_data).compared_percent_previous_day
    expected_data = dict(
        Open='1.60%',
        High='0.88%',
        Low='1.47%',
        Close='0.75%',
        Volume='0.45%'
    )
    assert compared_data == expected_data
    
def test_append_triangle(ohlcv_data, prev_ohlcv_data):
    """
    Test method for `Ohlcv().append_triangle`
    :param ohlcv: OHLCV data of stock price
    :type: hash
    :param prev_ohlcv: OHLCV data of stock price of yesterday
    :type: hash
    :return: Result assertion
    """
    ohlcv_instance = ohlcv.Ohlcv(ohlcv_data, prev_ohlcv_data)
    
    plus_number = 1000
    minus_number = -1000
    zero_number = 0
    
    expected_plus_str = '△1,000'
    expected_minus_str = '▲1,000'
    expected_zero_str = '0'
    
    appended_plus_number = ohlcv_instance.append_triangle(plus_number)
    appended_minus_number = ohlcv_instance.append_triangle(minus_number)
    appended_zero_number = ohlcv_instance.append_triangle(zero_number)

    assert appended_plus_number == expected_plus_str
    assert appended_minus_number == expected_minus_str
    assert appended_zero_number == expected_zero_str

def test_calc_percentage(ohlcv_data, prev_ohlcv_data):
    """
    Test method for `Ohlcv().calc_percentage()`
    :param ohlcv: OHLCV data of stock price
    :type: hash
    :param prev_ohlcv: OHLCV data of stock price of yesterday
    :type: hash
    :return: Result assertion
    """
    ohlcv_instance = ohlcv.Ohlcv(ohlcv_data, prev_ohlcv_data)
    
    current_number = 10000
    prev_number = 8000

    calcurated_percentage = ohlcv_instance.calc_percentage(current_number, prev_number)

    assert calcurated_percentage == '25.00%'
