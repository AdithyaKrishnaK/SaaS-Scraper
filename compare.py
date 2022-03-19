import json
import os
import pandas as pd

PATH = 'D:\Inter IIT\json\TWILIO INC\\10-K_2020-03-02.json'

# files = [name for name in os.listdir(PATH) if name.endswith('.txt')]
# for file in files:

with open(PATH,'r') as f:
    data = json.loads(f.read())
    b_sheet = data['BalanceSheets']

keys = b_sheet.keys()


list_data = b_sheet.get("StockholdersEquity")
list_row = {'name':["StockholdersEquity"]}
for i in list_data:
    val = i.get('value')
    date = i['period']['instant']
    list_row[date] = [val]

df = pd.DataFrame.from_dict(list_row)

for key in keys:
    list_data = b_sheet.get(key)
    list_row = {}
    list_row['name'] = key
    if type(list_data) is dict:
        val = list_data.get('value')
        date = list_data['period']['instant']
        list_row[date] = val
        continue

    for i in list_data:
        val = i.get('value')
        date = i['period']['instant']
        list_row[date] = val
    print(list_row)
    df = df.append(list_row,ignore_index = True)

df.to_csv("data.csv")
    


