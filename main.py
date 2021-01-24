"""
Python modules
csv: Perform operations such as extracting strings from a CSV file downloaded with stooq's API
datetime: Get a date for getting stock prices with stooq API
os: Get env file and delete csv and image files
join, dirname: Get env file
pandas: Read and sort data in a CSV file
mplfinance: Generate a chart image of stock price
pandas_datareader.stooq: API client for stooq
dateutil.relativedelta: Calculate the period of time for the stock price to be acquired

Internal module
slack: Notification Class to configure the settings for the Slack API
env: Module for geting environment variables from .env file
"""

import csv
import datetime
import os
import pandas as pd
import mplfinance as mpf
import pandas_datareader.stooq as stooq
from dateutil.relativedelta import relativedelta

import env
from notifiers import slack

today = datetime.date.today()


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
    stock_code = env.Env("stock_code").get()

    stooq_reader = stooq.StooqDailyReader(stock_code, start=start_date, end=today)
    stooq_reader.read().to_csv(f"/tmp/{str(today)}.csv")


# pylint: disable=W0613
def main(event, context):
    """
    The main function that will be executed when this Python file is executed
    """
    # tmp directory is present by default on Cloud Functions, so guard it
    if not os.path.isdir('/tmp'):
        os.mkdir('/tmp')

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


if __name__ == '__main__':
    # When main() is executed in CloudFunctions, (event,context) setted automatically in arguments
    # If main.oy is executed development environment, execute with (event: None, context: None)
    # https://cloud.google.com/functions/docs/writing/background?hl=ja#function_parameters
    main(None, None)
