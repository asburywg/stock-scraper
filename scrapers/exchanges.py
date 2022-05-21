import io
import json
from ftplib import FTP
from io import BytesIO
import pandas as pd

pd.set_option('display.max_columns', None)


def parse_status(status):
    """
    D = Deficient: Issuer Failed to Meet NASDAQ Continued Listing Requirements
    E = Delinquent: Issuer Missed Regulatory Filing Deadline
    Q = Bankrupt: Issuer Has Filed for Bankruptcy
    N = Normal (Default): Issuer Is NOT Deficient, Delinquent, or Bankrupt.
    G = Deficient and Bankrupt
    H = Deficient and Delinquent
    J = Delinquent and Bankrupt
    K = Deficient, Delinquent, and Bankrupt
    """
    if status == "D":
        return "Deficient"
    elif status == "E":
        return "Delinquent"
    elif status == "Q":
        return "Bankrupt"
    elif status == "N":
        return "Normal"
    elif status == "G":
        return "Deficient and Bankrupt"
    elif status == "H":
        return "Deficient and Delinquent"
    elif status == "J":
        return "Delinquent and Bankrupt"
    elif status == "K":
        return "Deficient, Delinquent, and Bankrupt"


def parse_exchange(x):
    """
    A = NYSE MKT
    N = New York Stock Exchange (NYSE)
    P = NYSE ARCA
    Z = BATS Global Markets (BATS)
    V = Investors' Exchange, LLC (IEXG)
    """
    if x == "A":
        return "NYSE MKT"
    elif x == "N":
        return "NYSE"
    elif x == "P":
        return "NYSE ARCA"
    elif x == "Z":
        return "BATS"
    elif x == "V":
        return "IEXG"


class Exchanges:
    """
    >>> ex = Exchanges()
    >>> ex.listed
    >>> ex.listed_json()

    http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs
    """

    def __init__(self):
        self.ftp = FTP('nasdaqtrader.com')
        self.ftp.login()
        self.listed = pd.concat([self._parse_file("symboldirectory/nasdaqlisted.txt", "NASDAQ"),
                                 self._parse_file("symboldirectory/otherlisted.txt", "other")])

        self.nasdaq = self.listed.loc[self.listed['Exchange'] == 'NASDAQ']['Symbol'].tolist()
        self.nyse = self.listed.loc[self.listed['Exchange'] == 'NYSE']['Symbol'].tolist()

        self.ftp.quit()

    def listed_json(self):
        return json.loads(self.listed.to_json(orient="records"))

    def _get_file(self, filename):
        r = BytesIO()
        self.ftp.retrbinary(f'RETR {filename}', r.write)
        return r.getvalue().decode("utf-8")

    def _parse_file(self, filename, exchange):
        data = self._get_file(filename)
        buffer = io.StringIO(data)
        df = pd.read_csv(buffer, sep="|", header='infer')
        df = df.rename(columns={"ACT Symbol": "Symbol", "Security Name": "Name"})
        df.drop(df.tail(1).index, inplace=True)
        df = df[~df['Symbol'].isna()]
        df = df.loc[(df['Test Issue'] == 'N')]
        df['Exchange'] = exchange if exchange == "NASDAQ" else df['Exchange'].apply(lambda x: parse_exchange(x))
        df['ETF'] = df['ETF'].apply(lambda x: False if x == "N" else True)
        if 'Financial Status' in df.columns:
            df['Financial Status'] = df['Financial Status'].apply(lambda x: parse_status(x))
        if 'Market Category' in df.columns:
            df['Market Category'] = df['Market Category'].apply(lambda x: "NASDAQ Global MarketSM" if x == "G" else (
                "NASDAQ Global Select MarketSM" if x == "Q" else "NASDAQ Capital Market"))
        df.drop(['Round Lot Size', 'NextShares', 'Test Issue', 'CQS Symbol', 'NASDAQ Symbol'], axis=1, inplace=True,
                errors='ignore')
        df['Name'] = df['Name'].apply(lambda x: x.replace('- Common Stock', '').replace('Common Shares', '').strip())
        return df

