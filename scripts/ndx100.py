import numpy as np
import bs4 as bs
import pickle 
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
from matplotlib import style

def saveTickers100():
    resp = requests.get("https://en.wikipedia.org/wiki/NASDAQ-100")
    soup = bs.BeautifulSoup(resp.text, features='lxml')
    table = soup.find('table', {'id' : "constituents"})
    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        tickers.append(ticker[:-1])
        
    with open("../pickles/ndx100tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers