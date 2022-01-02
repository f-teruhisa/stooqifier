"""
message: Test target class
"""

from message import message

def test__content(today_datetime, ohlcv_data, prev_ohlcv_data):
    """
    Test method for `Message().__content`
    :param ohlcv: OHLCV data of stock price
    :type: hash
    :param prev_ohlcv: OHLCV data of stock price of yesterday
    :type: hash
    :return: Result assertion
    """
    content = message.Message(today_datetime, ohlcv_data, prev_ohlcv_data).content
    expected_text = f"本日は{today_datetime.strftime('%Y年%m月%d日')}です。\n" \
               "取得可能な最新日付の株価情報をお知らせします。 \n\n" \
                    "*始値* 7,620 _[前日比: △120_ (1.60%)]\n" \
                    "*高値* 8,070 _[前日比: △70_ (0.88%)]\n" \
                    "*安値* 7,610 _[前日比: △110_ (1.47%)]\n" \
                    "*終値* 8,060 _[前日比: △60_ (0.75%)]\n" \
                    "*出来高* 823,700 _[前日比: △3,700_ (0.45%)]\n"
    assert content == expected_text

def test_format_data_to_message(today_datetime, ohlcv_data, prev_ohlcv_data):
    """
    Test method for `Message()._test_format_data_to_message()`
    :param ohlcv: OHLCV data of stock price
    :type: hash
    :param prev_ohlcv: OHLCV data of stock price of yesterday
    :type: hash
    :return: Result assertion
    """
    category = 'Open'
    formatted_message = message.Message(today_datetime, ohlcv_data, prev_ohlcv_data).format_data_to_message(ohlcv_data, category)
    expected_message = "7,620 _[前日比: △120_ (1.60%)]\n"
    
    assert formatted_message == expected_message
