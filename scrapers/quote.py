import requests
from bs4 import BeautifulSoup
from datetime import date


def decimal(dec):
    return float(dec.replace(',', '')) if dec != 'N/A' else None


class Quote:
    """
    >>> q = Quote("AAPL")
    >>> q.table  # raw
    >>> q.quote  # parsed
    """

    def __init__(self, symbol):
        self.symbol = symbol.replace('.', '-')
        self._source_url = f"https://finance.yahoo.com/quote/{symbol}"
        self._source = self._scrape_yf()
        self.table = self._get_quote()
        self.quote = {'symbol': self.symbol, **self._parse_table()}

    def _scrape_yf(self):
        response = requests.get(self._source_url)
        html = BeautifulSoup(response.text, 'html.parser')
        table_div = html.find('div', {'id': 'quote-summary'})
        return None if table_div is None else table_div.find_all('table')

    def _get_quote(self):
        table = {}
        for tab in self._source:
            table_body = tab.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = [ele.text.strip() for ele in row.find_all('td')]
                table[cols[0]] = cols[1]
        return table

    def _parse_table(self):
        days_range = self.table['Day\'s Range'].split(' - ')
        long_range = self.table['52 Week Range'].split(' - ')
        dividend = self.table['Forward Dividend & Yield'].split(' (')
        div_amount = dividend[0]
        div_percent = dividend[1].replace('%', '').replace(')', '')
        return {
            'date': str(date.today()),
            'previous_close': decimal(self.table['Previous Close']),
            'open': decimal(self.table['Open']),
            'bid': self.table['Bid'],
            'ask': self.table['Ask'],
            'day_range_low': decimal(days_range[0]),
            'day_range_high': decimal(days_range[1]),
            '52wk_range_low': decimal(long_range[0]),
            '52wk_range_high': decimal(long_range[1]),
            'volume': decimal(self.table['Volume']),
            'avg_volume': decimal(self.table['Avg. Volume']),
            'market_cap': self.table['Market Cap'],  # str to dec
            'beta_5y_mo': decimal(self.table['Beta (5Y Monthly)']) if self.table['Beta (5Y Monthly)'] != "N/A" else None,
            'pe_ttm': decimal(self.table['PE Ratio (TTM)']) if self.table['PE Ratio (TTM)'] != "N/A" else None,
            'eps_ttm': decimal(self.table['EPS (TTM)']) if self.table['EPS (TTM)'] != "N/A" else None,
            'earnings_date': self.table['Earnings Date'],
            'dividend_amount': decimal(div_amount),
            'dividend_percent': decimal(div_percent),
            'ex_div_date': self.table['Ex-Dividend Date'],
            '1yr_target': decimal(self.table['1y Target Est']) if self.table['1y Target Est'] != "N/A" else None
        }
