"""
Python modules
os: Get env file
join, dirname: Get env file path
dotenv: Get environment variants
"""

import os
from os.path import join, dirname
from dotenv import load_dotenv

class Env():
    """
    Enviroment variables(for Slack API token and Stock code) configure class
    """
    def __init__(self, key):
        self.key = str.upper(key)

    def get(self):
        """
        Load env variant with dotenv
        :return: String(In most case, depends on environment variables)
        """
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        return os.environ.get(self.key)

    def set(self, value):
        """
        # Write env variant's value with key
        """
        os.environ[self.key] = str(value)
