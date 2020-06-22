#!/usr/bin/env python3

import yfinance as yf
import os

msft = yf.Ticker("MSFT")

data = {k: str(v).encode("utf-8") for k,v in msft.info.items()}
print(data)
#print(msft.balance_sheet)

print("HELLO WORLD")

"""
Doesn't work right now, look later


os.environ["APCA_API_BASE_URL"] = "https://api.alpaca.markets"

api = tradeapi.REST('PKRQFM69CTHM63652ED2', 'X3Slm6uMg7NE4VAhjPZ8jEoKvOSgX3oOsD6LKQhR', api_version='v2') # or use ENV Vars shown below
#api = tradeapi.REST('PKRQFM69CTHM63652ED2', 'X3Slm6uMg7NE4VAhjPZ8jEoKvOSgX3oOsD6LKQhR')

account = api.get_account()
#api.list_positions()


#aapl = api.polygon.historic_agg_v2('AAPL', 1, 'day', _from='2019-01-01', to='2019-02-01').df
"""