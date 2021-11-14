import pandas as pd
import ccxt
from dateutil import parser


class PriceGetter:
    def __init__(self, exchange = "binance",symbol: str = 'DOGE/USDT', timeframe: str = "5m"):
        self.exchange_name = exchange
        if exchange == "binance":
            self.exchange = ccxt.binance()
        elif exchange == "coinbase":
            self.exchange = ccxt.coinbase()
        elif exchange == "cex":
            self.exchange = ccxt.cex()
        self.symbol = symbol
        self.timeframe = timeframe
        self.dfm = pd.DataFrame()

    def rank_data(self):
        self.dfm.sort_values("timestamp")

    def rename_col(self):
        self.dfm.rename({0: "timestamp", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume"},axis=1, inplace=True)

    def update_price(self, since, limit):
        if self.exchange_name == "binance":
            symbol = self.symbol
        elif self.exchange_name == "coinbase":
            symbol = self.symbol
        elif self.exchange_name == "cex":
            symbol=self.symbol[:-1]
        ohlcv = pd.DataFrame(self.exchange.fetch_ohlcv(symbol, self.timeframe, since, limit))
        self.dfm = self.dfm.append(ohlcv)

    def drop_duplicates(self):
        self.dfm = self.dfm.drop_duplicates()

    def save_price(self,filename: str="price_clean.csv"):
        self.dfm.to_csv(f"data/{filename}", index=False)

if __name__ == '__main__':
    price = PriceGetter(timeframe="5m")
    date = pd.read_csv("./data/doge_tweets.csv")["timestamp"]
    for d in date:
        if 4<=parser.parse(d).month<=10:
            timestamp = int(parser.parse(d).timestamp() ) * 1000 # daylight saving time
        else:
           timestamp = int(parser.parse(d).timestamp() - 3600*6) * 1000
        price.update_price(since=timestamp, limit=720)
    price.rename_col()
    price.drop_duplicates()
    price.rank_data()
    price.save_price("price_clean_6h.csv")
