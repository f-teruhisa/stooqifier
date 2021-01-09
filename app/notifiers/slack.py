"""
json: Format the data to be sent by the SLack API into JSON
requests: HTTP client
"""

import json
import requests

class Slack():
    """
    Notification Class to configure the settings for the Slack API
    """
    def __init__(self, webhook, date, stock_code, ohlcv):
        self.__webhook = webhook
        self.__date = date
        self.__stock_code = stock_code
        self.json = self.__json_dumps(ohlcv)

    @property
    def webhook(self):
        """
        Prpperty of Incoming Webhook of Slack
        :return: String(URI)
        """
        return self.__webhook

    @property
    def date(self):
        """
        Property of date to be displayed in Slack text
        :return: Date
        """
        return self.__date

    @property
    def stock_code(self):
        """
        Property of stock code to be displayed in Slack text
        :return: String
        """
        return self.__stock_code

    def __json_dumps(self, ohlcv):
        """
        Create JSON data for sending Slack notification with API.
        :param dict[str, str, str, str, str, str] ohlcv:
        :type ohlcv: {
            'Date': '2020-12-29',
            'Open': '7620',
            'High': '8070',
			'Low': '7610',
			'Close': '8060',
			'Volume': '823700'
        }
        """
        text = f"*始値* {int(ohlcv['Open']):,d}\n" \
			   f"*高値* {int(ohlcv['High']):,d}\n" \
			   f"*安値* {int(ohlcv['Low']):,d}\n" \
			   f"*終値* {int(ohlcv['Close']):,d}\n" \
			   f"*出来高* {int(ohlcv['Volume']):,d}"

        attachments = [{
			'title': f"{ohlcv['Date']}",
			'color': '#ffe44d',
			'text': text,
		}]

        data = json.dumps({
			"text": f"本日は{self.date.strftime('%Y年%m月%d日')}です。\n" \
					f"取得可能な最新日付の株価情報(銘柄: {self.stock_code})をお知らせします。",
			"attachments": attachments
		})

        return data

    def post(self):
        """
        POST request to Slack API
        """
        requests.post(self.webhook, data=self.json)
