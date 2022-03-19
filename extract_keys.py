import json
import os
from numpy import common_type
import pandas as pd

PATH = r"C:\Users\\adith\Desktop\Inter IIT\json"
req = ['PreferredStockSharesAuthorized','PreferredStockSharesIssued','CommonStockSharesAuthorized','CommonStockSharesIssued']
folders = [name for name in os.listdir(PATH)]
exhaustive = []
total = 0
for folder in folders:
    files = [name for name in os.listdir(os.path.join(PATH,folder)) if name.endswith('.txt') or name.endswith('.json')]
    for file in files:

        
        with open(os.path.join(PATH,folder,file),'r') as f:
            try:
                data = json.loads(f.read())
            except:
                continue
            
            b_sheet = data.get('BalanceSheets')
            
            if b_sheet == None:
                continue
            try:
                date = data['CoverPage']['DocumentPeriodEndDate']
            except:
                total +=1 
                continue
        keys = b_sheet.keys()
        entry = {"cik":data['CoverPage']['EntityCentralIndexKey']}
        for key in keys:
            if key in req:
                if type(b_sheet[key])==dict:
                    if b_sheet[key]['period']['instant']==date:
                        entry[key] = i['value']
                    continue
                for i in b_sheet[key]:
                    if i['period']['instant']==date:
                        
                        entry[key] = i['value']
        exhaustive.append(entry)

df = pd.DataFrame(exhaustive)
df.to_csv('share.csv')        

print(total)
