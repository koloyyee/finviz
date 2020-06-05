import pandas as pd
import pickle
import requests
import bs4 as bs
import os
from datetime import datetime as dt
import html5lib
import time 

current_month = dt.now().strftime("%m")
current_year = dt.now().strftime("%Y")
current_year_month = "{}-{}".format(current_year, current_month)

def scrape_from_finviz(ticker):

    url = 'https://finviz.com/quote.ashx?t={}'.format(ticker)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    try:
        req = requests.get(url, headers = headers)
        dfs = pd.read_html(req.text, attrs={"class":"snapshot-table2"})
        for df in dfs:
            if not os.path.exists('../stocksFunda-{}/{}{}.csv'.format(current_year_month, ticker, current_year_month)):
                try:
                    df.to_csv('../stocksFunda-{}/{}{}.csv'.format(current_year_month, ticker, current_year_month))
                    print("Saved {} on {} data".format(ticker, current_year_month))
                except KeyError:
                    print(ticker)
                    pass
            else:
                print('Already have {}'.format(ticker))  
    except Exception as e:
        print(e)
        pass
    

def scrape_500():
    with open('../pickles/sp500tickers.pickle', "rb") as f:
            tickers = pickle.load(f)    

    if not os.path.exists("../stocksFunda-{}".format(current_year_month)):
        os.makedirs("../stocksFunda-{}".format(current_year_month))
    for ticker in tickers:
        print("scraping {}".format(ticker))
        scrape_from_finviz(ticker)
    print("Done saving data")
    



def industry_scrape():
    url = "https://finviz.com/screener.ashx?v=111&f=ind_specialtyeateries"
    
    dfs = pd.read_html(url)
    industry_data = []
    dfs[-2].to_csv('../other_csv/special_eatery.csv')

def compile_data():
    with open('../pickles/sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)
    mainDf = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        if ticker == "BRK.B":
            pd.read_csv('../stocksFunda-{}/BRK-B{}.csv'.format(current_year_month,current_year_month))
        elif ticker == "BF.B":
            pd.read_csv('../stocksFunda-{}/BF-B{}.csv'.format(current_year_month,current_year_month))
        elif ticker == "TSS":
            pass
        else:
            df = pd.read_csv('stocksFunda-{}/{}{}.csv'.format(current_year_month, ticker, current_year_month))
            print(df.columns)

def ind_list():
    #bs4 way
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    res = requests.get("https://finviz.com/screener.ashx", headers = headers )
    soup=bs.BeautifulSoup(res.text, features="lxml")
    options = soup.find('select', {"id":"fs_ind"})
    inds = []
    try: 
        for menu in options.findAll('option')[2:-1]:
            inds.append(menu['value'])
        with open('../pickles/industries_list.pickle', 'wb') as f:
            pickle.dump(inds, f)
        print(inds)
        return inds
    except ValueError:
        pass

def  ind_top_20_comp(reload_inds=False, count =1):
    if reload_inds:
        inds = ind_list()
    else:
        with open('../pickles/industries_list.pickle', 'rb') as f:
            inds = pickle.load(f)
    
    for ind in inds:
        if ind == "medicalpractitioners":
            pass
        elif ind == "wholesaleother":
            pass
        else:
            url = "https://finviz.com/screener.ashx?v=161&f=ind_{}&o=-marketcap&r={}".format(ind, count)
            dfs = pd.read_html(url, attrs={"bgcolor": "#d3d3d3"}, header=0, index_col='No.')
            for df in dfs:
                try:
                    print('scraping {}'.format(ind))
                    df.to_csv('../ind_data-{}/{}{}.csv'.format(current_year_month,ind,current_year_month))
                except KeyError:
                    pass
                    print("Already have {}'s data".format(ind))
            print("Done scrapping {} list".format(ind))
        

def read_ind():

    df = pd.read_csv('../ind_data-2019-10/accidenthealthinsurance2019-10.csv')
    gb = df.groupby("Ticker")
    # comp = gb.get_group("AFL").set_index('Market Cap')
    ind_data = pd.DataFrame()
    values = df.sort_values('ROE')
    print(values)
    # for name, group in df.groupby("Ticker"):
    #     if ind_data.empty:
    #         print(group)
    #         ind_data = group.set_index("Market Cap")[["Market Cap"]].rename(columns={"Market Cap":name})
    #     else:
    #         ind_data = ind_data.join(group.set_index("Market Cap")[["Market Cap"]].rename(columns={"Market Cap":name}))
    # ind_data.head()
start_time = time.time()
scrape_500()
print("%s " % (time.time()-start_time))