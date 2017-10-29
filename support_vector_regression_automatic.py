
from sklearn.svm import SVR 
from yahoo_finance import Share 
import numpy as np 
import urllib2
from BeautifulSoup import BeautifulSoup as bs
import pandas as pd 
import json

def get_historical_data(name, number_of_days):
    data = []
    url = "https://finance.yahoo.com/quote/" + name + "/history/"
    rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')

    for each_row in rows:
        divs = each_row.findAll('td')
        if divs[1].span.text  != 'Dividend':
            data.append({'Date': divs[0].span.text, 'Open': float(divs[1].span.text.replace(',',''))})

    return data[:number_of_days]


def predict_prices(prices, days_to_predict_in_future): 
    days = np.arange(0,len(stock_list), 1) 
    prices = (np.asarray(prices)).reshape(-1, 1)
    days = days.reshape(-1, 1) 
    svr_rbf = SVR(kernel = 'rbf', C=1e3, gamma = 0.1) 
    svr_rbf.fit(days, prices.ravel()) 
    predict_days = (int(days_to_predict_in_future))
    max_day = 2 + max(days) + predict_days
    min_day = max(days) + 2 
    days_to_predict = np.arange(min_day, max_day, 1) 
    days_to_predict = days_to_predict.reshape(-1, 1)
    
    return svr_rbf.predict(days_to_predict)

df = pd.read_csv("NYSEcut.csv")


SVR_symbol_list = [] 
SVR_predictions = [] 
bad_SVR = [] 


for cell in (df['symbols']): 
    past_days = 365
    future_days = 10 
    #try: 
    data = get_historical_data(cell, int(past_days))
    stock_list = [] 
    for i in data:
        stock_list.append((i['Open']))
    pred = predict_prices(stock_list, future_days)
    SVR_symbol_list.append(cell)
    SVR_predictions.append(pred)
    SVR_predictions_file = open('SVR_pred.txt', 'w')
    SVR_predictions_file.write("%s\n" % pred)
    SVR_predictions_file.write("%s\n" % "/")
    print("done")
    #with open('SVR_predictions', 'w') as f1:
    #    f1.write(json.dumps(SVR_predictions))
    #with open('SVR_symbol_list', 'w') as f2:
    #    f2.write(json.dumps(SVR_symbol_list))
    #except: 
    #    print(cell)
    #    print("failed")
    #    bad_SVR.append(cell)
    #    with open('bad_SVR', 'w') as fout3:
    #        json.dump(bad_SVR, fout3)
