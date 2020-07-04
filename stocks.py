#!/usr/bin/env python3

import yfinance as yf
import os
import argparse
import requests
import time
import unicodedata
import psycopg2
import datetime
import matplotlib.pyplot as plt
import random
import signal
import sys
from pandas_datareader import data as pdr
from bs4 import BeautifulSoup

class Stock():
    
    def __init__(self, name, P1, P2, P3, P4):
        self.name = name
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4

    def to_string(self):
        return "P1: {}, P2: {}, P3: {}, P4: {}".format(self.P1, self.P2, self.P3, self.P4)

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
    parser.add_argument("-p", "--sp", help="Select the S&P500 as your selected stocks", default=False, action="store_true")
    parser.add_argument("-e", "--end", help="End date in YYYY-MM-DD format", required=True)
    parser.add_argument("-s", "--start", help="Start date in YYYY-MM-DD format", required=True)
    parser.add_argument("-i", "--init", help="Initial investment for the bot", required=True)
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

    stock_data = dict()
    
    for tag in Tickers:
        try:
            print("Working on : {}".format(tag))
            data = pdr.get_data_yahoo(tag, start=start, end=end)
            stock_data[tag] = data
        except:
            continue

    all_stocks = list()
    legends = list()
    stocks_class = list()
    for day in range((end - (start)).days):
        
        mu = 0
        for tag in Tickers:
            try:
                opn = stock_data[tag].loc[day, "Open"]
                close = stock_data[tag].loc[day, "Close"]
                mu = mu + ((close-opn)/opn)
            except:
                continue

        mu = mu / len(Tickers)

        for tag in Tickers:
            curr_day = start + datetime.timedelta(days=day)
            
            try:
                opn = stock_data[tag].loc[day, "Open"]
                close = stock_data[tag].loc[day, "Close"]
                low = stock_data[tag].loc[day, "Low"]
                high = stock_data[tag].loc[day, "High"]
                adj = stock_data[tag].loc[day, "Adj Close"]

                stocks_class.append(Stock(tag, (close - opn)/opn, args.i/len(Tickers), \
                    ((close - opn)/opn) - mu, adj - close))
            except:
                continue
        
    """for i in stock_data.keys():
        for index, row in stock_data[i].iterrows():
            print("INDEX: {}, ROW: {}, NAME: {}".format(index, row, i))"""

    for stock in stocks_class:
        print(stock.to_string())


    """for i in Tickers:
        for j in range((end - (start)).days):
            day = start + datetime.timedelta(days=j)
            try:
                d[day] = stock_data[i].loc[day, "High"]
                opn = stock_data[i].loc[day, "Open"]
                close = stock_data[i].loc[day, "Close"]
                low = stock_data[i].loc[day, "Low"]
                high = stock_data[i].loc[day, "High"]

                stocks_class.append(Stock(tag, (opn - close)/ open, args.i/len(Tickers)))
            except:
                continue

        color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        plot = plt.plot_date(d.keys(), d.values(), 'b-', label=i, c=color)"""

    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    #plt.show()