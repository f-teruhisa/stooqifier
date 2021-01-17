"""
Python modules
csv: Perform operations such as extracting strings from a CSV file downloaded with stooq's API
datetime: Get a date for getting stock prices with stooq API
os: Get env file and delete csv and image files
join, dirname: Get env file
pandas: Read and sort data in a CSV file
mplfinance: Generate a chart image of stock price
pandas_datareader.stooq: API client for stooq
dotenv: Get environment variants
dateutil.relativedelta: Calculate the period of time for the stock price to be acquired

Internal module
slack: Notification Class to configure the settings for the Slack API
"""

import csv
import datetime
import os
from os.path import join, dirname
import pandas as pd
import mplfinance as mpf
import pandas_datareader.stooq as stooq
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

from notifiers import slack

def generate_stock_chart_image():
    """
    Generate a six-month stock chart image with mplfinance
    """
    dataframe = pd.read_csv(f"/tmp/{str(today)}.csv", index_col=0, parse_dates=True)
    # The return value `Date` from stooq is sorted by asc, so change it to desc for plot
    dataframe = dataframe.sort_values('Date')
    mpf.plot(dataframe, type='candle', figratio=(12,4),
         volume=True, mav=(5, 25), style='yahoo',
         savefig=f"/tmp/{str(today)}.png")

def generate_csv_with_datareader():
    """
    Generate a csv file of OHLCV with date with stooq API
    """
    start_date = today - relativedelta(months=3)
    stooq_reader = stooq.StooqDailyReader(stock_code, start=start_date, end=today)
    stooq_reader.read().to_csv(f"/tmp/{str(today)}.csv")

# pylint: disable=W0613
# When main() is executed in CloudFunction, (event,context) are automatically specified as arguments
# https://cloud.google.com/functions/docs/writing/background?hl=ja#function_parameters
def main(event, context):
    """
    The main function that will be executed when this Python file is executed
    """
    generate_csv_with_datareader()
    generate_stock_chart_image()
    with open(f"/tmp/{str(today)}.csv", 'r', encoding="utf-8") as file:
        # Skip header row
        reader = csv.reader(file)
        header = next(reader)
        for i, row in enumerate(csv.DictReader(file, header)):
            # Send only the most recent data to Slack notification
            if i == 0:
                slack.Slack(today, row).post()

# Load env variants
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
stock_code = os.environ.get("STOCK_CODE")

# Get today's date for getting the stock price and csv&image filename
today = datetime.date.today()

# tmp directory is present by default on Cloud Functions, so guard it
if not os.path.isdir('/tmp'):
    os.mkdir('/tmp')

FILENAME = '%s.csv' % str(today)
