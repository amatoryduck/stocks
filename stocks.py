#!/usr/bin/env python3

import yfinance as yf
import os
import argparse
import requests
import time
import unicodedata
from bs4 import BeautifulSoup

class Stock():
    
    def __init__(self, name):
        self.name = name

def get_Dow():
    Dow_Website = requests.get("https://money.cnn.com/data/dow30/")
    soup = BeautifulSoup(Dow_Website.content, "html.parser")

    Dow_Table = soup.find("table", {"class": "wsod_dataTable wsod_dataTableBig"})
    rows = Dow_Table.find_all("tr")
    Dow_data = list()

    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        Dow_data.append([ele for ele in cols if ele])

    Dow_tags = list()
    for company in Dow_data:
        if company != []:
            name = unicodedata.normalize("NFKD", company[0])
            tag = name.split(" ")[0]
            Dow_tags.append(tag)

    return Dow_tags

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

if __name__=="__main__":
    parser = argparse.ArgumentParser("stocks")
    parser.add_argument("-d", "--dow", help="Select the Dow Jones as your selected stocks", default=False, action="store_true")
    parser.add_argument("-s", "--sp", help="Select the Dow Jones as your selected stocks", default=False, action="store_true")
    args = parser.parse_args()

    if args.dow == False and args.sp == False:
        raise Exception("You need to select a market")

    stocks = set()
    Tickers = set()

    if args.dow:
        Tickers = Tickers.union(set(get_Dow()))
    if args.sp:
        Tickers = Tickers.union(set(get_SP()))

    for tag in Tickers:
        try:
            print("Working on : {}".format(tag))
            ticker = yf.Ticker(tag)
        except:
            continue
        