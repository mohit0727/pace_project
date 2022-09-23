import pymongo
import requests

from bs4 import BeautifulSoup
from pprint import pprint

COLUMN_TO_INDEX_MAP = {
    'name': 2,
    'price': 3,
    'oneHour': 4,
    'twentyFourHour': 5,
    'sevenDay': 6,
    'marketCap': 7,
    'volume': 8
}
session = requests.session()
url = 'https://coinmarketcap.com/'
try:
    response = session.get(url)
    response.raise_for_status()
    content = response.content
except requests.RequestException as ec:
    print(ec)

soup = BeautifulSoup(content, 'lxml')
table = soup.find('table', {"class":"h7vnx2-2 juYUEZ cmc-table"})
body = table.find('tbody')
trs = body.find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    doc = {}
    for key in COLUMN_TO_INDEX_MAP:
        index = COLUMN_TO_INDEX_MAP[key]
        doc[key] = tds[index].getText()
    pprint(doc)
    exit()
