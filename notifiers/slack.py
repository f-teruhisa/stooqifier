"""
Python modules
requests: HTTP client

Internal module
env: Module for geting environment variables from .env file
"""

import requests
import env

class Slack():
    """
    Notification Class to configure the settings for the Slack API
    """
    def __init__(self, date, ohlcv):
        self.__date = date
        self.text = self.__format_text(ohlcv)
        self.params = self.__params_dumps()

    @property
    def date(self):
        """
        Property of date to be displayed in Slack text
        :return: Date
        """
        return self.__date

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
               f"*始値* {int(ohlcv['Open']):,d}\n" \
			   f"*高値* {int(ohlcv['High']):,d}\n" \
			   f"*安値* {int(ohlcv['Low']):,d}\n" \
			   f"*終値* {int(ohlcv['Close']):,d}\n" \
			   f"*出来高* {int(ohlcv['Volume']):,d}"
        return text

    def __params_dumps(self):
        """
        Setting parameters when request with slack's files.upload API
        API docs: https://api.slack.com/methods/files.upload
        :return: dict
        """
        token = env.Env('slack_api_token').get()
        channel_id = env.Env('slack_channel_id').get()

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
        url = "https://slack.com/api/files.upload"
        file = {'file': open(f"/tmp/{str(self.date)}.png", 'rb')}
        request = requests.post(url=url, params=self.params, files=file)

        # Output response from the Slack API with requests
        print(request.status_code)
        print(request.text)
