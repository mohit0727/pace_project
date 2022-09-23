import time
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
    'volume': 8,
    'supply': 9
}
session = requests.session()

url = 'https://coinmarketcap.com/'
host_url = 'http://127.0.0.1:5000/'

while True:
    time.sleep(5)
    try:
        response = session.get(url)
        response.raise_for_status()
        content = response.content
    except requests.RequestException as ec:
        print(ec)

    soup = BeautifulSoup(content, 'lxml')
    table = soup.find('table')
    if not table:
        print('No table found')
        continue
    body = table.find('tbody')
    if not body:
        print('No body found')
        continue
    trs = body.find_all('tr')
    if not trs:
        print('No trs found')
        continue
    data = []
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) < 8:
            continue
        doc = {}
        for key in COLUMN_TO_INDEX_MAP:
            index = COLUMN_TO_INDEX_MAP[key]
            if key in ['oneHour', 'twentyFourHour', 'sevenDay']:
                td = tds[index]
                up_span = td.find('span', {'class': 'icon-Caret-up'})
                if up_span:
                    doc[key + '_sign'] = 'up'
                down_span = td.find('span', {'class': 'icon-Caret-down'})
                if down_span:
                    doc[key + '_sign'] = 'down'
            if key == 'marketCap':
                td = tds[index]
                span = td.find('span', {"data-nosnippet": "true"})
                doc[key] = span.getText()
            elif key == 'volume':
                td = tds[index]
                span = td.find('div', {"data-nosnippet": "true"})
                doc[key] = span.getText()
            else:
                doc[key] = tds[index].getText()
        data.append(doc)
        post_url = host_url + 'setData'
    response = session.post(post_url, json={'results': data})
    if response.status_code == 200:
        print('Inserted Docs')
