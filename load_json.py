import json
from pprint import pprint

with open('data_list_saved') as data_file:    
    data = json.load(data_file)
    print(data[0])
