import json
import xmltodict
import requests

"""

WIP

"""

SEC_CIK = {
    "Altimeter": "0001825200",
    "Elon Musk": "0001494730",
    "Bridgewater": "0001350694",
    "Jeff Bezos": "0001043298",
    "Mark Zuckerberg": "0001548760",
    "Palihapitiya Chamath": "0001715450",
    "Buffett Warren E": "0000315090",
    "Bill & Melinda Gates Foundation": "0001663801",
    "Loeb Daniel S": "0001300345"
}
headers = {'User-Agent': "your@email.com"}


def fetch(url):
    try:
        res = requests.get(url, headers=headers)
    except:
        return None
    if res.status_code != 200:
        print(f"{res.status_code} - {res.text}")
        return None
    return res


def scrape_sec():
    for cik in SEC_CIK.values():
        subs = fetch(f"https://data.sec.gov/submissions/CIK{cik}.json").json()
        print(json.dumps(subs))
        filings = subs.get("filings").get("recent")
        for num, doc in zip(filings.get('accessionNumber'), filings.get('primaryDocument')):
            doc = doc.split('/')[1] if '/' in doc else doc
            url = f"https://sec.report/Document/{num}/{doc}"
            res = fetch(url).text.strip()
            if '<HTML>' in res:
                continue
            xml = xmltodict.parse(res)
            print(json.dumps(xml))


# issuerTradingSymbol
# transactionCode https://www.sec.gov/edgar/searchedgar/ownershipformcodes.html
# https://sec.report/Document/0001104659-21-080869/tm2119689d1_4.xml
# https://www.sec.gov/edgar/sec-api-documentation
# https://sec.report/CIK

scrape_sec()
