import pandas as pd
import numpy as np

data = pd.read_json('../data_list_saved')
names = pd.read_json('../stock_names_saved')

nameddata = dict()

for i, row in names.iterrows():
    nameddata[row[0]] = {
        'name': row[0],
        'data': [],
        'startDate': data[0][0]['Date'],
        'endDate': data[len(data) - 1][0]['Date']
    }

prevcol = None
for col in data:
    currcol = data[col]
    date = data[col][np.nonzero(data[col])[0][0]]['Date']
    for i in range(len(currcol)):
        if not currcol[i] :
            currcol[i] = {'Date': date, 'Open': prevcol[i]['Open']}
    data[col] = currcol
    prevcol = currcol

print(data)

for col in data:
    currcol = data[col]
    for i in range(len(currcol)):
        nameddata[names[0][i]]['data'].append(currcol[i])

def getdata(symbol):
    return nameddata[symbol]
