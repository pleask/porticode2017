import json

with open('data_list_saved.json') as json_file:
    data_input = json.load(json_file)

with open('stock_names_saved.json') as json_file:
    data_names = json.load(json_file)

def get_data(symb):
    data_list = []
    num = 0
    # get number assigned to the symb name from data names
    for i in data_names[0]:
        if i == symb:
            num = i 
    # use number in outputting correct list from data_input
    for j in range(len(data_input[num])):
        data_list.append(data_input[num][j]['Open'])

    return data_list
