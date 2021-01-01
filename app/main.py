"""
Get a csv of the stock price for one year of the stock specified by STOCK_CODE in .env with pandas_datareader.
After that, delete the csv file.
"""
import datetime
import os
from os.path import join, dirname
import pandas_datareader.stooq as stooq
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

today = datetime.date.today()
start_date = today - relativedelta(years=1)
end_date = today

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
stock_code = os.environ.get("STOCK_CODE")

stooq_reader = stooq.StooqDailyReader(stock_code, start=start_date, end=end_date)
data = stooq_reader.read()
FILENAME = '%s.csv' % str(today)
data.to_csv(FILENAME)
os.remove(FILENAME)
