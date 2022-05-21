import json
import yfinance as yf


class PriceHistory:
    """
    >>> ph = PriceHistory(["AAPL", "TSLA"])
    >>> ph.quotes.get("AAPL")

    https://github.com/ranaroussi/yfinance
    """

    def __init__(self, symbols):
        tickers = " ".join(symbols) if type(symbols) == list else " ".join(symbols.split(","))
        self.tickers = tickers.replace('.', '-')
        self.quotes = self._download_price_history()

    def _download_price_history(self):
        data = yf.download(self.tickers, period='max', group_by='ticker', timeout=10)
        result = {}
        for s in self.tickers.split(" "):
            df = data[s]
            df = df[df.Volume.notnull()]
            result[s] = json.loads(df.to_json(orient="records"))
        return result

