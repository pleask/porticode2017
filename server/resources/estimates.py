import pandas as pd
import json

datafilename = "../preddata.json"
namesfilename = "../NYSEcut.csv"

with open(datafilename) as in_file:
    data = json.load(in_file)


names = pd.read_csv(namesfilename)


datadict = {}
for i, name in names.iterrows():
    datadict[name.values[0]] = data[i]
print(datadict)

def get_estimate(symbol):
    return datadict[symbol]
