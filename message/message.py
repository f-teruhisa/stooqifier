"""
ohlcv: OHLCV calculation value class module
"""
from message import ohlcv

# pylint: disable=R0903
# Too few public methods (1/2) (too-few-public-methods)
# The number of public methods has been reduced due to devide the class responsibilities.
class Message():
    """
    Value object class for notification message
    """

    def __init__(self, date, ohlcv_data, prev_ohlcv_data):
        data = ohlcv.Ohlcv(ohlcv_data, prev_ohlcv_data)
        self.date = date
        self.prev_compared_ohlcv = data.compared_numbers_previous_day
        self.prev_compared_percent_ohlcv = data.compared_percent_previous_day
        self.content = self.__content(ohlcv_data)

    def __content(self, ohlcv_data):
        """
        Create params data for sending Slack notification with API.
        :param ohlcv_data: OHLCV data of stock price
        :type ohlcv_data: hash
            example: {
            'Date': '2020-12-29',
            'Open': '7620',
            'High': '8070',
            'Low': '7610',
            'Close': '8060',
            'Volume': '823700'
        }
        :return: String
        """
        text = f"本日は{self.date.strftime('%Y年%m月%d日')}です。\n" \
               f"取得可能な最新日付の株価情報をお知らせします。 \n\n" \
               f"*始値* {self.format_data_to_message(ohlcv_data, 'Open')}" \
               f"*高値* {self.format_data_to_message(ohlcv_data, 'High')}" \
               f"*安値* {self.format_data_to_message(ohlcv_data, 'Low')}" \
               f"*終値* {self.format_data_to_message(ohlcv_data, 'Close')}" \
               f"*出来高* {self.format_data_to_message(ohlcv_data, 'Volume')}"
        return text

    def format_data_to_message(self, ohlcv_data, category):
        """
        Format message with ohlcv data
        :param ohlcv_data: OHLCV data of stock price
        :type ohlcv_data: hash
        :param category: Any of the items in OHLCV
        :type string
        :return: string
        """
        current = f"{int(ohlcv_data[f'{category}']):,d} "
        compared_number = f"_[前日比: {self.prev_compared_ohlcv[f'{category}']}_ "
        compared_percentage = f"({self.prev_compared_percent_ohlcv[f'{category}']})]\n"
        message = current + compared_number + compared_percentage
        return message
