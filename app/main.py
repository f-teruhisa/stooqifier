"""
Get a csv of the stock price for one year specified by STOCK_CODE in .env with pandas_datareader.
After that, delete the csv file.
"""
import csv
import datetime
import os
from os.path import join, dirname
import json
import pandas as pd
import mplfinance as mpf
import pandas_datareader.stooq as stooq
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
import requests

def send_slack_notification(row_dict):
    """
    Send notification with Slack.
    row_dict: {
        'Date': '2020-12-29',
        'Open': '7620',
        'High': '8070',
        'Low': '7610',
        'Close': '8060',
        'Volume': '823700'
    }
    """
    text = f"*始値* {int(row_dict['Open']):,d}\n" \
           f"*高値* {int(row_dict['High']):,d}\n" \
           f"*安値* {int(row_dict['Low']):,d}\n" \
           f"*終値* {int(row_dict['Close']):,d}\n" \
           f"*出来高* {int(row_dict['Volume']):,d}"

    attachments = [{
        'title': f"{row_dict['Date']}",
        'color': '#ffe44d',
        'text': text,
    }]

    data = json.dumps({
        "text": f"本日は{today.strftime('%Y年%m月%d日')}です。\n取得可能な最新日付の株価情報(銘柄: {stock_code})をお知らせします。",
        "attachments": attachments
    })
    requests.post(webhook, data=data)

def generate_stock_chart_image():
    """
    Generate a six-month stock chart image with mplfinance
    """
    dataframe = pd.read_csv(FILENAME, index_col=0, parse_dates=True)
    # The return value `Date` from stooq is sorted by asc, so change it to desc for plot
    dataframe = dataframe.sort_values('Date')
    mpf.plot(dataframe, type='candle', figratio=(12,4),
         volume=True, mav=(5, 25), style='yahoo',
         savefig=f"{str(today)}.png")

today = datetime.date.today()
start_date = today - relativedelta(months=3)
end_date = today

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
stock_code = os.environ.get("STOCK_CODE")
webhook = os.environ.get("INCOMING_WEBHOOK")

stooq_reader = stooq.StooqDailyReader(stock_code, start=start_date, end=end_date)
stooq_data = stooq_reader.read()
FILENAME = '%s.csv' % str(today)
file = stooq_data.to_csv(FILENAME)

with open(FILENAME, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for i, row in enumerate(csv.DictReader(f, header)):
        if i == 0:
            send_slack_notification(row)

generate_stock_chart_image()

# Remove files(if the files remains, they will be accumulated as garbage)
os.remove(FILENAME)
os.remove(f"{str(today)}.png")
