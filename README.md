# Stock Scraper

### S&P 500 Companies
Parse [List of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) wiki for index constituents and change events in the index. 

```
[
    {
        "symbol": "MMM",
        "company": "3M",
        "sector": "Industrials",
        "industry": "Industrial Conglomerates",
        "headquarters": "Saint Paul, Minnesota",
        "date_first_added": "1976-08-09",
        "cik": "0000066740",
        "founded": "1902"
    },
    ...
]
```

Events:
```
[
    {
        "date": "2022-04-04",
        "symbol_added": "CPT",
        "company_added": "Camden",
        "symbol_removed": "PBCT",
        "company_removed": "People's United Financial",
        "reason": "S&P 500 constituent M&T Bank Corp. acquired People’s United Financial."
    },
    ...
]
```

### Exchanges
Fetches stock listings for NASDAQ/NYSE exchanges from nasdaqtrader's FTP server, [docs](http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs)

```
[
    {
        "Symbol": "AAPL",
        "Name": "Apple Inc.",
        "Market Category": "NASDAQ Global Select MarketSM",
        "Financial Status": "Normal",
        "ETF": false,
        "Exchange": "NASDAQ"
    },
    ...
]
```

### Price History
Downloads stock's full price history from Yahoo Finance with [yfinance](https://github.com/ranaroussi/yfinance) package.
```
{"AAPL": [{"Date": "1980-12-12", "Open": 0.1283479929, "High": 0.1289059967, "Low": 0.1283479929, "Close": 0.1283479929, "Adj Close": 0.1001784727, "Volume": 469033600.0}, ... ]}
```

### Current Quote
Parses Yahoo Finance summary table for a stock, [example](https://finance.yahoo.com/quote/AAPL)

```
{
    "MMM": {
        "date": "2022-05-21",
        "previous_close": 146.96,
        "open": 147.54,
        "bid": "143.70 x 900",
        "ask": "144.22 x 1100",
        "day_range_low": 141.09,
        "day_range_high": 147.94,
        "52wk_range_low": 139.74,
        "52wk_range_high": 206.81,
        "volume": 4195356.0,
        "avg_volume": 3308612.0,
        "market_cap": "82.882B",
        "beta_5y_mo": 0.97,
        "pe_ttm": 14.23,
        "eps_ttm": 10.11,
        "earnings_date": "Apr 25, 2022 - Apr 29, 2022",
        "dividend_amount": 5.96,
        "dividend_percent": 3.99,
        "ex_div_date": "May 19, 2022",
        "1yr_target": 158.36
    },
    ...
}
```

#### Profile
Queries Yahoo Finance for profile data (industry, sector, etc.)
More data available, [example](https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=assetProfile%2CsummaryProfile%2CsummaryDetail%2CesgScores%2Cprice%2CincomeStatementHistory%2CincomeStatementHistoryQuarterly%2CbalanceSheetHistory%2CbalanceSheetHistoryQuarterly%2CcashflowStatementHistory%2CcashflowStatementHistoryQuarterly%2CdefaultKeyStatistics%2CfinancialData%2CcalendarEvents%2CsecFilings%2CrecommendationTrend%2CupgradeDowngradeHistory%2CinstitutionOwnership%2CfundOwnership%2CmajorDirectHolders%2CmajorHoldersBreakdown%2CinsiderTransactions%2CinsiderHolders%2CnetSharePurchaseActivity%2Cearnings%2CearningsHistory%2CearningsTrend%2CindustryTrend%2CindexTrend%2CsectorTrend)

```
{
    "MMM": {
        "industry": "Conglomerates",
        "sector": "Industrials",
        "summary": "3M Company operates as a diversified technology company worldwide. It operates through four segments: Safety and Industrial; Transportation and Electronics; Health Care; and Consumer. The Safety and Industrial segment offers industrial abrasives and finishing for metalworking applications; autobody repair solutions; closure systems for personal hygiene products, masking, and packaging materials; electrical products and materials for construction and maintenance, power distribution, and electrical original equipment manufacturers; structural adhesives and tapes; respiratory, hearing, eye, and fall protection solutions; and natural and color-coated mineral granules for shingles. The Transportation and Electronics segment provides ceramic solutions; attachment tapes, films, sound, and temperature management for transportation vehicles; premium large format graphic films for advertising and fleet signage; light management films and electronics assembly solutions; packaging and interconnection solutions; and reflective signage for highway, and vehicle safety. The Healthcare segment offers food safety indicator solutions; health care procedure coding and reimbursement software; skin, wound care, and infection prevention products and solutions; dentistry and orthodontia solutions; and filtration and purification systems. The Consumer segment provides consumer bandages, braces, supports and consumer respirators; cleaning products for the home; retail abrasives, paint accessories, car care DIY products, picture hanging, and consumer air quality solutions; and stationery products. It offers its products through e-commerce and traditional wholesalers, retailers, jobbers, distributors, and dealers. The company was founded in 1902 and is based in St. Paul, Minnesota.",
        "employees": 95000,
        "country": "United States"
    },
    ...
}
```
