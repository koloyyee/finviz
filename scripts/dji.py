import numpy as np
import pandas as pd
# import pandas_datareader as web
import bs4 as bs
import pickle
import requests
import datetime as dt

def saveDJTickers():
    response = requests.get('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')
    soup = bs.BeautifulSoup(response.text, features='lxml')
    table = soup.find('table', {'id': 'constituents'})
    tickers = []

   
    for row in table.findAll('tr')[1:]:
        td = row.findAll('td')[2]
        ticker = td.find('a', {'class':'external text'}).text
        tickers.append(ticker)
    
    with open("../pickles/dji_tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    
    print(tickers)
    return tickers
saveDJTickers()