#!/usr/bin/env python3

import yfinance as yf
import os
import argparse
import requests
import time
from bs4 import BeautifulSoup

class Stock():
    
    def __init__(self, name):
        self.name = name

def get_SP(): 
    SP_Website = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(SP_Website.content, "html.parser")

    SP_Table = soup.find("table", {"id": "constituents"})
    SP_table_body = SP_Table.find('tbody')
    rows = SP_table_body.find_all('tr')
    SP_data = list()

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        SP_data.append([ele for ele in cols if ele])

    SP_tags = list()
    for company in SP_data:
        if company != []:
            SP_tags.append(company[0])

    return SP_tags

"""msft = yf.Ticker("ABBV")
print(msft.info)
data = {k: str(v).encode("utf-8") for k,v in msft.info.items()}
print(data)

for k, v in msft.info.items():
    print("K : {}, \tV: {}".format(k, v))"""


if __name__=="__main__":
    SP_Tags = get_SP()
    stocks = list()
    Tickers = list()

    for tag in SP_Tags:
        try:
            ticker = yf.Ticker(tag)
            print("WORKING ON TAG: {}".format(tag))
            #ticker_data = {k: str(v).encode("utf-8") for k,v in ticker.info.items()}
            #print(ticker_data)
            print(ticker.info)
            #time.sleep(5)
        except:
            continue
        