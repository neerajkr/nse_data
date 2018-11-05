#!/usr/bin/env python3
import string
import json
import csv
from bs4 import BeautifulSoup
import requests

url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=BANKNIFTY&date=6NOV2018'

headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}


r = requests.get(url,headers=headers)
html = r.text
soup = BeautifulSoup(html,'html.parser')
data = []
table = soup.find('div', attrs={'class':'opttbldata'})

# table header parse
table_header = table.find('thead')
row = table_header.find_all('tr')[1] # ignore first row
cols = row.find_all('th')
cols = ([ele.text.strip() for ele in cols])[1:-1]  # ignore first and last column
data.append(cols)

rows = table.find_all('tr')[2:-1]
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

import csv
with open("nse_options_chain.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)
