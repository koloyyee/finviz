import os
import pickle 
import requests
import pandas as pd
import pandas_datareader as web
import bs4 as bs
from datetime import datetime as dt
import pandas_datareader as web


current_month = dt.now().strftime("%m")
current_year = dt.now().strftime("%Y")
current_year_month = "{}-{}".format(current_year, current_month)

def saveHSI():
    response = requests.get("http://www.aastocks.com/tc/stocks/market/index/hk-index-con.aspx")
    soup = bs.BeautifulSoup(response.text, features="lxml")
    table = soup.find('table',{'class': "tblM s2"})
    symbols=[]
    for row in table.findAll('tr')[1:]:
        symbol = row.findAll('a')[0].text
        # title = symbol.find('a', {"class":"a14 cls"}).text
        symbols.append(symbol[:-3])
    with open('../pickles/hsiConSymbolHalf.pickle', 'wb') as f:
        pickle.dump(symbols, f)    
    print(symbols)
    return symbols

def get_data_from_aastock(symbol):
    url="http://www.aastocks.com/tc/stocks/analysis/company-fundamental/financial-ratios?symbol={}".format(symbol)
    # dfs = pd.read_html(url, attrs={'id':'cnhk-list'})
    dfs = pd.read_html(url)

    print(dfs)
    for df in dfs:
        if not os.path.exists('../hsiFunda-{}/{}{}.csv'.format(current_year_month, symbol, current_year_month)):
            try:
                df.to_csv('../hsiFunda-{}/{}-{}.csv'.format(current_year_month, symbol, current_year_month))
                print("Saved {} on {} data".format(symbol, current_year_month))
            except KeyError:
                pass
        else:
            print('Already have {}'.format(symbol))  
get_data_from_aastock('00001')
# def scrape_hsi(reload_aastock=False):
    
#     if reload_aastock:
#         symbols = saveHSI()
#     else:
#         with open('hsiConSymbolHalf.pickle', 'rb') as f:
#             symbols = pickle.load(f)
#     if not os.path.exists('hsiFunda{}'.format(current_year_month)):
#         os.makedirs('hsiFunda{}'.format(current_year_month))
#     for symbol in symbols:
#         get_data_from_aastock(symbol)
    
#     print("Done saving data")
# scrape_hsi()
        