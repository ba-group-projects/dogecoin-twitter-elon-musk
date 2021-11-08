import pandas as pd
import yfinance as yf
from dateutil import parser
import datetime


class PriceGetter:
    def get_tesla_share_price(self):
        """
        Get the current share price of Tesla.
        """
        ticker = yf.Ticker("TSLA")
        price = ticker.history(start='2021-01-01')
        return price

    def get_nasdaq_share_price(self):
        """
        Get the current share price of NASDAQ.
        """
        ticker = yf.Ticker("^NDX")
        price = ticker.history(start='2021-01-01')
        return price

    def get_and_save_data(self):
        nasdaq = self.get_nasdaq_share_price()
        tesla = self.get_tesla_share_price()
        # merge nasdaq and tesla on index
        merged = nasdaq.merge(tesla, left_index=True, right_index=True)
        merged.rename(
            {'Close_x': 'Close_NASDAQ', 'Close_y': 'Close_Tesla', "High_x": "High_NASDAQ", "High_y": "High_Tesla",
             "Low_x": "Low_NASDAQ", "Low_y": "Low_Tesla", "Volume_x": "Volume_NASDAQ", "Volume_y": "Volume_Tesla",
             "Open_x": "Open_NASDAQ", "Open_y": "Open_Tesla", "Dividends_x": "Dividends_NASDAQ",
             "Dividends_y": "Dividends_Tesla", "Stock Splits_x": "Stock Splits_NASDAQ",
             "Stock Splits_y": "Stock Splits_Tesla"},
            axis=1, inplace=True)
        merged.to_csv("./data/share_price.csv")


class PriceCleaner:

    def __init__(self, dfm):
        self.dfm = dfm

    def get_and_save_data(self, date: list):
        self.cal_increase_rate()
        self.cal_excess_increase_rate()
        self.find_the_next_trading_date(date)
        self.dfm.to_csv("./data/share_price_clean.csv")

    def cal_increase_rate(self):
        self.dfm["Increase_rate_nasdaq"] = self.dfm["Close_NASDAQ"].pct_change()
        self.dfm["Increase_rate_tesla"] = self.dfm["Close_Tesla"].pct_change()

    def cal_excess_increase_rate(self):
        self.dfm["Excess_increase_rate"] = self.dfm["Increase_rate_tesla"] - self.dfm["Increase_rate_nasdaq"]

    def find_the_next_trading_date(self, date_list: list):
        dfm = pd.DataFrame()
        while date_list:
            date_list = list(map(lambda x: parser.parse(x).strftime("%Y-%m-%d"), date_list))
            temp_dfm = self.dfm[self.dfm["Date"].apply(lambda x: x in date_list)]
            dfm = dfm.append(temp_dfm)
            for i in temp_dfm["Date"].to_list():
                while i in date_list:
                    date_list.remove(i)
            date_list =list(map(lambda x: (parser.parse(x)+datetime.timedelta(days=1)).strftime("%Y-%m-%d"), date_list))
        self.dfm = dfm
        return self.dfm


if __name__ == "__main__":
    pg = PriceGetter()
    pg.get_and_save_data()
    dfm = pd.read_csv("./data/share_price.csv")
    date = pd.read_csv("./data/tweets_clean.csv").datetime.tolist()
    pc = PriceCleaner(dfm)
    pc.get_and_save_data(date)
