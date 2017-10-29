import json
import pandas as pd

with open ('../sentiment_list_saved') as data_file:
    data = json.load(data_file)

names = pd.read_csv('../NYSEcut.csv')

print(len(data), len(names)) #wtf??
