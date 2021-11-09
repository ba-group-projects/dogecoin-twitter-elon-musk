import pandas as pd
import ccxt


class PriceGetter:
    def __init__(self, symbol: str = 'DOGE/USDT', timeframe: str = "1m"):
        self.binance = ccxt.binance()
        self.symbol = symbol
        self.timeframe = timeframe
        self.dfm = pd.DataFrame()

    def update_price(self,since,limit):
        ohlcv = self.binance.fetch_ohlcv(self.symbol, self.timeframe,since,limit)
        self.dfm.append(ohlcv)

    def save_price(self):
        pass


last = print_chart(binance, symbol, timeframe)
print("\n" + binance.name + " ₿ = $" + str(last) + "\n")  # print last closing price
