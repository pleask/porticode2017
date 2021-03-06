from sklearn.svm import SVR
from yahoo_finance import Share
import numpy as np
import urllib2
import pandas as pd
from BeautifulSoup import BeautifulSoup as bs
import json


number_of_days = 365 * 2

def get_historical_data(name, number_of_days):
    data = []
    url = "https://finance.yahoo.com/quote/" + name + "/history/"
    rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')

    for each_row in rows:
        divs = each_row.findAll('td')
        if divs[1].span.text  != 'Dividend':
            data.append({'Date': divs[0].span.text, 'Open': float(divs[1].span.text.replace(',',''))})

    return data[:number_of_days]


df = pd.read_csv("./NYSEcut.csv")

data_list = []
cell_list = []
bad_list = [] 

count = 0

for cell in (df['symbols']):
    try:
        data_list.append(get_historical_data(cell, number_of_days))
        count = count + 1
        print(count)
        cell_list.append(cell) 
    except:
        print(bad_list.append(cell))

with open('stock_names_saved', 'w') as fout:
    json.dump(cell_list, fout)


with open('data_list_saved', 'w') as fout2:
    json.dump(data_list, fout2)

with open('bad_list_saved', 'w') as fout2:
    json.dump(bad_list, fout2)
