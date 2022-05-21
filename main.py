import json
import time
import logging as log

from scrapers.exchanges import Exchanges
from scrapers.price_history import PriceHistory
from scrapers.profile import YahooFinance
from scrapers.quote import Quote
from scrapers.sp500 import SP500

log.basicConfig(level=log.DEBUG)


def write_json(data, filename, timestamp=True, pretty_print=True, directory="./data"):
    ts = f"_{int(time.time())}" if timestamp else ""
    with open(f'{directory}/{filename}{ts}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4 if pretty_print else None)


def get_symbols(persist=True):
    result = {}
    # S&P 500
    sp = SP500()
    result['SP500'] = sp.symbols
    print(f"S&P 500 events: {sp.get_events()}")
    # Exchanges (NASDAQ / NYSE)
    ex = Exchanges()
    result['NASDAQ'] = ex.nasdaq
    result['NYSE'] = ex.nyse
    # write results
    if persist:
        write_json(sp.constituents, 'sp500')
        write_json(ex.listed_json(), 'exchanges')
    return result


def get_price_history(tickers):
    log.debug(f"Fetching price history")
    ph = PriceHistory(tickers)
    write_json(ph.quotes, "price_history", False, False)


def get_profiles(tickers):
    profiles = {}
    for sym in tickers:
        log.debug(f"Fetching profile: {sym}")
        profiles[sym] = YahooFinance(sym).profile
    write_json(profiles, "profiles", False)


def get_current_quotes(tickers):
    results = {}
    for sym in tickers:
        log.debug(f"Fetching current quote: {sym}")
        results[sym] = Quote(sym).quote
    write_json(results, "current_quotes")


def main():
    stocks = get_symbols(persist=False)
    tickers = stocks.get('SP500')
    get_price_history(tickers)
    get_profiles(tickers)
    get_current_quotes(tickers)


main()
