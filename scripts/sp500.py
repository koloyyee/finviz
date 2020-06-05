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

style.use('ggplot')


def saveTickers500():
    response=requests.get( 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(response.text, features="lxml")
    table = soup.find('table',{'class' : "wikitable sortable"})
    tickers=[]
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker[:-1])
    with open('../pickles/sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers

def getDataFromYahoo(reloadSp500=False):
    if reloadSp500:
        tickers = saveTickers500()
    else:
        with open('../pickles/sp500tickers.pickle', 'rb') as f: 
            tickers = pickle.load(f)
    if not os.path.exists('stockDFs'):
        os.makedirs('stockDFs')
    start = dt.datetime(2000,1,1)
    end = dt.datetime.now()

    for ticker in  tickers:
        if not os.path.exists('../stockDFs/{}.csv'.format(ticker)):
            try:
                df=web.DataReader(ticker, 'yahoo' ,start, end)
                df.to_csv('../stockDFs/{}.csv'.format(ticker))
                print("Done scraping with {}".format(ticker))
            except KeyError:
                pass
        else:
            print('Already have {}'.format(ticker))  

def compileData():
    with open('../sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)
    mainDf = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv('../other_csv/stockDFs/{}.csv'.format(ticker))
        print(df)
        df.set_index('Date', inplace=True)
        df.rename(columns={'Adj Close' : ticker}, inplace=True)
        df.drop(['Open', 'High','Low', 'Close', 'Volume'], 1, inplace=True)
    #     if mainDf.empty:
    #         mainDf=df
    #     else :
    #         mainDf= mainDf.join(df, how='outer')
    #     if count %10 == 0:
    #         print(count)
    # print (mainDf.tail())
    # mainDf.to_csv('sp500joint.csv')
compileData()

def visualize_data():
    df = pd.read_csv('../other_csv/sp500joint.csv')
    # df['AAPL'].plot()
    # plt.show()
    df_corr = df.corr()
    print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    heatmap= ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0])+ 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1])+ 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()


# visualize_data()