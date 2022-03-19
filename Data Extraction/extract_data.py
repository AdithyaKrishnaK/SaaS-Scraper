import json
import os
import pandas as pd
import pickle

PATH = r"C:\Users\\adith\Desktop\Inter IIT\json"
PATH_PE = r"pe_ratio.json"
PATH_PM = r"pm_ratio.json"
PATH_REVENUE = r"revenue_10-K_full.json"
OPEN_IE = r"C:\Users\adith\Desktop\Inter IIT\Pckl"

folders = [name for name in os.listdir(PATH)]
exhaustive = []
total = 0
final_data = {}
for folder in folders:
    files = [name for name in os.listdir(os.path.join(PATH,folder)) if name.endswith('.txt') or name.endswith('.json')]
    for file in files:
       
        with open(os.path.join(PATH,folder,file),'r') as f:
            try:
                data = json.loads(f.read())
                date = data['CoverPage']['DocumentPeriodEndDate']
                cik = data['CoverPage']['EntityCentralIndexKey']
            except:
                print(folder,file)
                continue
            
            for section in ['StatementsOfIncome','BalanceSheets','StatementsOfCashFlows']:
    
                b_sheet = data.get(section)
                if b_sheet == None:
                    print("error",folder,file)
                    continue

                if final_data.get(section)==None:
                    final_data[section] = {}
                sheet = final_data[section]
                
                for entry in b_sheet.keys():
                    list_data = b_sheet.get(entry)
                    
                    if sheet.get(entry)==None:
                        sheet[entry] = []

                    list_row = sheet[entry]
                    
                    if type(list_data) is dict:
                        val = list_data.get('value')
                        try:
                            entry_date = list_data['period']['endDate']
                        except:
                            entry_date = list_data['period']['instant']
                        if date == entry_date:
                            list_row.append({entry_date:val})
                        continue

                    for i in list_data:
                        try:
                            val = i.get('value')
                        except:
                            print(i)
                            continue
                        try:
                            entry_date = i['period']['endDate']
                        except:
                            entry_date = i['period']['instant']
                        if date == entry_date:
                            list_row.append({entry_date:val})
                            
                            break;
                    
                    sheet[entry] = list_row
                    
                
    analytics = {}   

    with open(PATH_PE,'r') as m:
        data = json.loads(m.read())     
        try:
            analytics['PE'] = data.get(folder)
        except:
            print('Analytics error')
    with open(PATH_PM,'r') as m:
        data = json.loads(m.read())     
        try:
            analytics['PM'] = data.get(folder)
        except:
            print('Analytics error')
    with open(PATH_REVENUE,'r') as m:
        data = json.loads(m.read())     
        try:
            analytics['Revenue'] = data.get(folder)
        except:
            print('Analytics error')
    final_data['Analytics'] = analytics

    filename = cik+'.json'
    with open(os.path.join('data',filename),'a') as m:
        json.dump(final_data,m)

    
    


# print(final_data)
