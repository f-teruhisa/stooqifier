"""
json: Format the data to be sent by the SLack API into JSON
requests: HTTP client
"""

import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests

class Slack():
    """
    Notification Class to configure the settings for the Slack API
    """

    def __init__(self, date, text):
        self.__date = date
        self.text = text
        self.params = self.__params_dumps()

    @property
    def date(self):
        """
        Property of date to be displayed in Slack text
        :return: Date
        """
        return self.__date

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
            'token': token,
            'channels': channel_id,
            'filename': f"{str(self.date)}.png",
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
        requests.post(url="https://slack.com/api/files.upload", params=self.params, files=file)
