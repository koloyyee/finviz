import numpy as np
import pandas as pd
import pickle
from collections import Counter
from sklearn.model_selection import cross_validate ,train_test_split
from sklearn import svm, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

def processDataForLabels(ticker):
    hmDays=7
    df = pd.read_csv('other_csv/sp500joint.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hmDays+1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) -df[ticker]) / df[ticker]
    
    df.fillna(0, inplace=True)
    return tickers, df

def buySellHold(*args):
    cols = [c for c in args]
    requirements = 0.02
    for col in cols:
        if col > requirements:
            return 1
        if col < -requirements:
            return -1
    return 0

def extractFeatureSets(ticker):
    tickers, df = processDataForLabels(ticker)

    df['{}_target'.format(ticker)] = list(map( buySellHold,
                                               df['{}_1d'.format(ticker)],
                                               df['{}_2d'.format(ticker)],
                                               df['{}_3d'.format(ticker)],
                                               df['{}_4d'.format(ticker)],
                                               df['{}_5d'.format(ticker)],
                                               df['{}_6d'.format(ticker)],
                                               df['{}_7d'.format(ticker)] ))
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print ('Data spread', Counter(str_vals))
    df.fillna(0, inplace=True)

    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True )

    X  = df_vals.values
    y = df['{}_target'.format(ticker)].values

    return X, y, df

def doML(ticker):

    X, y, df = extractFeatureSets('XOM')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

    # clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.SVC(gamma="auto")),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('Accuracy', confidence )
    predictions = clf.predict(X_test)
    print('Predicted spread: ', Counter(predictions))

    return confidence
doML('SHAK')