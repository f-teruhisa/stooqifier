"""
Python modules
datetime: Get the date for test date.
message: Test target class
"""

import datetime
from message import message

def test__content(ohlcv, prev_ohlcv):
    """
    Test method for Message().__content
    :param ohlcv: Hash
    :param prev_ohlcv: Hash
    :return: Result assertion
    """
    date = datetime.date(2020, 12, 28)
    content = message.Message(date, ohlcv, prev_ohlcv).content
    expected_text = "本日は2020年12月28日です。\n" \
               "取得可能な最新日付の株価情報をお知らせします。 \n\n" \
                    "*始値* 7,620 _[前日比: △120_ (1.60%)]\n" \
                    "*高値* 8,070 _[前日比: △70_ (0.88%)]\n" \
                    "*安値* 7,610 _[前日比: △110_ (1.47%)]\n" \
                    "*終値* 8,060 _[前日比: △60_ (0.75%)]\n" \
                    "*出来高* 823,700 _[前日比: △3,700_ (0.45%)]\n"
    assert content == expected_text
