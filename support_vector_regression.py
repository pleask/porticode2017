from sklearn.svm import SVR 
from yahoo_finance import Share 
import numpy as np 
import urllib2
from BeautifulSoup import BeautifulSoup as bs


stock_code = raw_input("What stock code do you want to predict? ")
past_days = raw_input("Number of past days to input to model: ") 
future_days = raw_input("Number of future days to predict: ")


def get_historical_data(name, number_of_days):
    data = []
    url = "https://finance.yahoo.com/quote/" + name + "/history/"
    rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')

    for each_row in rows:
        divs = each_row.findAll('td')
        if divs[1].span.text  != 'Dividend':
            data.append({'Date': divs[0].span.text, 'Open': float(divs[1].span.text.replace(',',''))})

    return data[:number_of_days]


data = get_historical_data(stock_code, int(past_days))


stock_list = [] 


for i in data:
  stock_list.append((i['Open']))


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

print(predict_prices(stock_list, future_days))
