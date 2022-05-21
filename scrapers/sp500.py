import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class SP500:
    """
    >>> sp = SP500()
    >>> sp.symbols
    >>> sp.constituents
    >>> sp.get_events()
    """
    SOURCE_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def __init__(self):
        self._source = self._scrape_wiki()
        self.constituents = self._get_constituents()
        self.symbols = [x['symbol'] for x in self.constituents]

    def _scrape_wiki(self):
        response = requests.get(self.SOURCE_URL)
        return BeautifulSoup(response.text, 'html.parser')

    def _get_constituents(self):
        table = self._source.find('table', id="constituents")
        rows = table.findAll('tr')
        row_data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) != 0:
                data = [ele.text.strip() for ele in cols]
                row_data.append(data)

        result = []
        for row in row_data:
            result.append({"symbol": row[0], "company": row[1], "sector": row[3], "industry": row[4],
                           "headquarters": row[5], "date_first_added": row[6], "cik": row[7], "founded": row[8]})
        return result

    def get_events(self):
        table = self._source.find_all('tbody')[1]
        rows = table.find_all('tr')
        results = []
        for row in rows:
            cols = [x.text.strip() for x in row.find_all('td')]
            if len(cols) != 0:
                results.append({'date': datetime.strftime(datetime.strptime(cols[0], '%B %d, %Y'), '%Y-%m-%d'),
                                'symbol_added': cols[1], 'company_added': cols[2], 'symbol_removed': cols[3],
                                'company_removed': cols[4], 'reason': re.sub("[\(\[].*?[\)\]]", "", cols[5])})
        return results

