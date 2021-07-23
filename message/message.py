"""
re: Matching with regex for appending plus/minus into number of stock price
"""
import re

class Message():
    """
    Value object class for noitification message
    """

    def __init__(self, date, ohlcv, prev_ohlcv):
        self.date = date
        self.prev_compared_ohlcv = self.__compared_numbers_previous_day(ohlcv, prev_ohlcv)
        self.prev_compared_percent_ohlcv = self.__compared_percet_previous_day(ohlcv, prev_ohlcv)
        self.content = self.__content(ohlcv)

    def __content(self, ohlcv):
        """
        Create params data for sending Slack notification with API.
        :param dict[str, str, str, str, str, str] ohlcv:
        :type ohlcv: {
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
               f"*始値* {self.format_data_to_message(ohlcv, 'Open')}" \
               f"*高値* {self.format_data_to_message(ohlcv, 'High')}" \
               f"*安値* {self.format_data_to_message(ohlcv, 'Low')}" \
               f"*終値* {self.format_data_to_message(ohlcv, 'Close')}" \
               f"*出来高* {self.format_data_to_message(ohlcv, 'Volume')}"
        return text

    def format_data_to_message(self, ohlcv, category):
        """
        Format message with ohlcv data
        :param ohlcv:
        :param category:
        :return: string
        """
        current = f"{int(ohlcv[f'{category}']):,d} "
        compared_number = f"_[前日比: {self.prev_compared_ohlcv[f'{category}']}_ "
        compared_percentage = f"({self.prev_compared_percent_ohlcv[f'{category}']})]\n"
        message = current + compared_number + compared_percentage
        return message

    @classmethod
    def __compared_percet_previous_day(cls, ohlcv, prev_ohlcv):
        """
        Compare ohlcv percentage data with prev_ohlcv.
        :param dict[str, str, str, str, str, str] ohlcv:
        :type ohlcv, prev_ohlcv: {
            'Date': '2020-12-29',
            'Open': '7620',
            'High': '8070',
            'Low': '7610',
            'Close': '8060',
            'Volume': '823700'
        }
        :return: dict
        """
        prev_compared_percentage_ohlcv = dict(
            Open=cls.calc_percentage_ohlcv(int(ohlcv['Open']), int(prev_ohlcv['Open'])),
            High=cls.calc_percentage_ohlcv(int(ohlcv['High']), int(prev_ohlcv['High'])),
            Low=cls.calc_percentage_ohlcv(int(ohlcv['Low']), int(prev_ohlcv['Low'])),
            Close=cls.calc_percentage_ohlcv(int(ohlcv['Close']), int(prev_ohlcv['Close'])),
            Volume=cls.calc_percentage_ohlcv(int(ohlcv['Volume']), int(prev_ohlcv['Volume']))
        )
        return prev_compared_percentage_ohlcv

    @classmethod
    def calc_percentage_ohlcv(cls, current, prev):
        """
        Calculate compare percentage with previous day
        (current_numbers / previous_day_number) / previous_day_number
        :param current:
        :param prev:
        :return: string
        """
        percentage = '{:.2%}'.format((int(current) - int(prev)) / int(prev))
        return percentage

    @classmethod
    def __compared_numbers_previous_day(cls, ohlcv, prev_ohlcv):
        """
        Compare ohlcv data with prev_ohlcv.
        :param dict[str, str, str, str, str, str] ohlcv:
        :type ohlcv, prev_ohlcv: {
            'Date': '2020-12-29',
            'Open': '7620',
            'High': '8070',
            'Low': '7610',
            'Close': '8060',
            'Volume': '823700'
        }
        :return: dict
        """
        prev_compared_ohlcv = dict(
            Open=cls.append_triangle(int(ohlcv['Open']) - int(prev_ohlcv['Open'])),
            High=cls.append_triangle(int(ohlcv['High']) - int(prev_ohlcv['High'])),
            Low=cls.append_triangle(int(ohlcv['Low']) - int(prev_ohlcv['Low'])),
            Close=cls.append_triangle(int(ohlcv['Close']) - int(prev_ohlcv['Close'])),
            Volume=cls.append_triangle(int(ohlcv['Volume']) - int(prev_ohlcv['Volume']))
        )
        return prev_compared_ohlcv

    @classmethod
    def append_triangle(cls, number):
        """
        Add ▲ when the previous day's value is negative
        and △ when the previous day's value is positive
        in front of the number.
        :param number:
        :return: number:
        """
        is_minus = re.match(r'-', str(number))

        if is_minus:
            appended_number = str('{:,}'.format(number)).replace('-', '▲')
        elif number == 0:
            appended_number = '{:,}'.format(number)
        else:
            appended_number = '△' + str('{:,}'.format(number))

        return appended_number
