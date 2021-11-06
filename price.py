import yfinance as yf


def get_tesla_share_price():
    """
    Get the current share price of Tesla.
    """
    ticker = yf.Ticker("TSLA")
    price = ticker.history(start='2021-01-01')
    price.to_csv("data/share_price.csv")


if __name__ == '__main__':
    get_tesla_share_price()
