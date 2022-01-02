"""
re: Matching with regex for appending plus/minus into number of stock price
"""
import re

class Ohlcv():
    """
    Value object class for OHLCV calculation
    """
    def __init__(self, ohlcv, prev_ohlcv):
        """
        Compare ohlcv percentage data with prev_ohlcv.
        :param ohlcv: OHLCV data of stock price
        :type
            ohlcv: hash
            example: {
            'Date': '2020-12-29',
            'Open': '7620',
            'High': '8070',
            'Low': '7610',
            'Close': '8060',
            'Volume': '823700'
        }
        :param prev_ohlcv: OHLCV data of stock price of yesterday
        :type
            prev_ohlcv: hash
            example: {
            'Date': '2020-12-29',
            'Open': '7620',
            'High': '8070',
            'Low': '7610',
            'Close': '8060',
            'Volume': '823700'
        }
        """
        self.ohlcv = ohlcv
        self.prev_ohlcv = prev_ohlcv
        self.compared_numbers_previous_day = self.__compared_numbers_previous_day()
        self.compared_percent_previous_day = self.__compared_percent_previous_day()

    def __compared_numbers_previous_day(self):
        """
        Compare ohlcv data with previous ohlcv.
        :return: dict
        """
        prev_compared_ohlcv = dict(
            Open=self.append_triangle(int(self.ohlcv['Open']) - int(self.prev_ohlcv['Open'])),
            High=self.append_triangle(int(self.ohlcv['High']) - int(self.prev_ohlcv['High'])),
            Low=self.append_triangle(int(self.ohlcv['Low']) - int(self.prev_ohlcv['Low'])),
            Close=self.append_triangle(int(self.ohlcv['Close']) - int(self.prev_ohlcv['Close'])),
            Volume=self.append_triangle(int(self.ohlcv['Volume']) - int(self.prev_ohlcv['Volume']))
        )
        return prev_compared_ohlcv

    @staticmethod
    def append_triangle(number):
        """
        Add ▲ when the previous day's value is negative
        and △ when the previous day's value is positive
        in front of the number.
        :param number: Number of the target to be given a triangle
        :type: number
        :return: string
        """
        is_minus = re.match(r'-', str(number))

        if is_minus:
            appended_number = str('{:,}'.format(number)).replace('-', '▲')
        elif number == 0:
            appended_number = '{:,}'.format(number)
        else:
            appended_number = '△' + str('{:,}'.format(number))

        return appended_number

    def __compared_percent_previous_day(self):
        """
        Compare ohlcv percentage data with previous ohlcv.
        :return: dict
        """
        prev_compared_percentage_ohlcv = dict(
            Open=self.calc_percentage(int(self.ohlcv['Open']), int(self.prev_ohlcv['Open'])),
            High=self.calc_percentage(int(self.ohlcv['High']), int(self.prev_ohlcv['High'])),
            Low=self.calc_percentage(int(self.ohlcv['Low']), int(self.prev_ohlcv['Low'])),
            Close=self.calc_percentage(int(self.ohlcv['Close']), int(self.prev_ohlcv['Close'])),
            Volume=self.calc_percentage(int(self.ohlcv['Volume']), int(self.prev_ohlcv['Volume']))
        )
        return prev_compared_percentage_ohlcv

    @staticmethod
    def calc_percentage(current, prev):
        """
        Calculate compare percentage with previous day
        (current_number / previous_day_number) / previous_day_number
        :param current: current_number
        :param prev: previous_day_number
        :return: string
        """
        percentage = '{:.2%}'.format((int(current) - int(prev)) / int(prev))
        return percentage
