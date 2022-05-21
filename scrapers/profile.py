from scrapers.common import fetch


class YahooFinance:
    """
    https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
    """

    def __init__(self, symbol):
        self.symbol = symbol.replace('.', '-')
        self._source_url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=assetProfile%2CsummaryProfile%2CsummaryDetail%2CesgScores%2Cprice%2CincomeStatementHistory%2CincomeStatementHistoryQuarterly%2CbalanceSheetHistory%2CbalanceSheetHistoryQuarterly%2CcashflowStatementHistory%2CcashflowStatementHistoryQuarterly%2CdefaultKeyStatistics%2CfinancialData%2CcalendarEvents%2CsecFilings%2CrecommendationTrend%2CupgradeDowngradeHistory%2CinstitutionOwnership%2CfundOwnership%2CmajorDirectHolders%2CmajorHoldersBreakdown%2CinsiderTransactions%2CinsiderHolders%2CnetSharePurchaseActivity%2Cearnings%2CearningsHistory%2CearningsTrend%2CindustryTrend%2CindexTrend%2CsectorTrend"
        self.data = self._fetch_data()
        self.profile = self._parse_profile() if self.data else None
        # TODO: explore more data available
        # print(list(data.keys()))
        # self.recommendations = data.get('recommendationTrend').get('trend')

    def _parse_profile(self):
        if "assetProfile" not in self.data:
            return None
        return {
            "industry": self.data.get('assetProfile').get('industry'),
            "sector": self.data.get('assetProfile').get('sector'),
            "summary": self.data.get('assetProfile').get('longBusinessSummary'),
            "employees": self.data.get('assetProfile').get('fullTimeEmployees'),
            "country": self.data.get('assetProfile').get('country')
        }

    def _fetch_data(self):
        res = fetch(self._source_url)
        if res:
            result = res.json().get('quoteSummary').get('result')
            return result[0] if result else None
        return None
