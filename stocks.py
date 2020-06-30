#!/usr/bin/env python3

import yfinance as yf
import os
import argparse
import requests
import time
import unicodedata
import psycopg2
import datetime
from pandas_datareader import data as pdr
from bs4 import BeautifulSoup

class Stock():
    
    def __init__(self, name):
        self.name = name

def setup_DB():
    con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port="5432")
    print("Database opened successfully")   

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
    parser.add_argument("-p", "--sp", help="Select the Dow Jones as your selected stocks", default=False, action="store_true")
    parser.add_argument("-e", "--end", help="End date in YYYY-MM-DD format", required=True)
    parser.add_argument("-s", "--start", help="Start date in YYYY-MM-DD format", required=True)
    args = parser.parse_args()

    try:
        start = datetime.datetime.strptime(args.start, "%Y-%m-%d")
    except:
        raise Exception("Start date must be in YYYY-MM-DD format")

    try:
        end = datetime.datetime.strptime(args.end, "%Y-%m-%d")
    except:
        raise Exception("End date must be in YYYY-MM-DD format")

    print("{} {}".format(start, end))

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
            data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
            print(data)
            #ticker = yf.Ticker(tag)
        except:
            continue
        
        