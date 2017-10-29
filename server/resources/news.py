import json
import pandas as pd

with open ('../sentiment_list_saved') as data_file:
    data = json.load(data_file)
with open ('../stock_Description_saved') as data_file:
    names = json.load(data_file)
namesymbols = pd.read_csv('../NYSEcut.csv')


symbols = []
for i, name in enumerate(names):
    matchvals = namesymbols.loc[namesymbols['Description'] == name]['symbols'].values
    if len(matchvals):
        symbols.append((namesymbols.loc[namesymbols['Description'] == name]['symbols'].values[0]))
    else:
        symbols.append(None)

sentiment_data = pd.DataFrame({'symbol':symbols, 'name':names, 'sentiment':data})
outdata = sentiment_data[pd.notnull(sentiment_data['symbol'])]

# tojson = outdata.drop('sentiment', axis = 1)
# tojson = tojson.to_dict('records')
#
# with open("newssentiment.json", 'w') as outfile:
#     json.dump(tojson, outfile)


def newssentiment(symbol):
    response =  (outdata[outdata['symbol'] == symbol]['sentiment'].values[0])
    return response
