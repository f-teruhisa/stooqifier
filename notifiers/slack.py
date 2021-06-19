"""
json: Format the data to be sent by the SLack API into JSON
requests: HTTP client
"""

import os
from os.path import join, dirname
import re
from dotenv import load_dotenv
import requests

class Slack():
    """
    Notification Class to configure the settings for the Slack API
    """
    def __init__(self, date, ohlcv, prev_ohlcv):
        self.__date = date
        self.prev_compared_ohlcv = self.__compare_previous_day(ohlcv, prev_ohlcv)
        self.text = self.__format_text(ohlcv)
        self.params = self.__params_dumps()

    @property
    def date(self):
        """
        Property of date to be displayed in Slack text
        :return: Date
        """
        return self.__date

    @classmethod
    def __compare_previous_day(cls, ohlcv, prev_ohlcv):
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
            appended_number = str(number).replace('-', '▲')
        elif number == 0:
            appended_number = number
        else:
            appended_number = '△' + str(number)

        return appended_number

    def __format_text(self, ohlcv):
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
               f"取得可能な最新日付の株価情報をお知らせします。 \n\n"\
               f"*始値* {int(ohlcv['Open']):,d} _(前日比: {self.prev_compared_ohlcv['Open']})_\n" \
			   f"*高値* {int(ohlcv['High']):,d} _(前日比: {self.prev_compared_ohlcv['High']})_\n" \
			   f"*安値* {int(ohlcv['Low']):,d} _(前日比: {self.prev_compared_ohlcv['Low']})_\n" \
			   f"*終値* {int(ohlcv['Close']):,d} _(前日比: {self.prev_compared_ohlcv['Close']})_\n" \
			   f"*出来高* {int(ohlcv['Volume']):,d} _(前日比: {self.prev_compared_ohlcv['Volume']})_"
        return text

    def __params_dumps(self):
        """
        Setting parameters when request with slack's files.upload API
        API docs: https://api.slack.com/methods/files.upload
        :return: dict
        """
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        token = os.environ.get("SLACK_API_TOKEN")
        channel_id = os.environ.get("SLACK_CHANNEL_ID")

        params = {
            'token':token,
            'channels':channel_id,
            'filename':f"{str(self.date)}.png",
            'initial_comment': self.text,
            'title': f"{str(self.date)}.png"
        }

        return params

    def post(self):
        """
        POST request to Slack file upload API
        API docs: https://api.slack.com/methods/files.upload
        """
        file = {'file': open(f"/tmp/{str(self.date)}.png", 'rb')}
        requests.post(url="https://slack.com/api/files.upload",params=self.params, files=file)
