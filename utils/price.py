import pandas as pd
import ccxt
from dateutil import parser

class PriceGetter:
    def __init__(self, symbol: str = 'DOGE/USDT', timeframe: str = "1m"):
        self.binance = ccxt.binance()
        self.symbol = symbol
        self.timeframe = timeframe
        self.dfm = pd.DataFrame()

    def rank_data(self):
        self.dfm.sort_values("timestamp")

    def rename_col(self):
        self.dfm.rename({0: "timestamp", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume"},axis=1, inplace=True)

    def update_price(self, since, limit):
        ohlcv = pd.DataFrame(self.binance.fetch_ohlcv(self.symbol, self.timeframe, since, limit))
        self.dfm = self.dfm.append(ohlcv)

    def drop_duplicates(self):
        self.dfm = self.dfm.drop_duplicates()

    def save_price(self):
        self.dfm.to_csv(f"data/price_clean.csv", index=False)

if __name__ == '__main__':
    price = PriceGetter()
    date = pd.read_csv("./data/doge_tweets.csv")["timestamp"]
    for d in date:
        timestamp = int(parser.parse(d).timestamp() - 3600) * 1000
        price.update_price(since=timestamp, limit=120)
    price.rename_col()
    price.drop_duplicates()
    price.rank_data()
    price.save_price()
