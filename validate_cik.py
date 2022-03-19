# import pandas as pd
# import requests
# import json

# BASE_URL_CIK = 'https://data.sec.gov/submissions/'
# cik_df = pd.read_csv('result/res.csv', usecols=['name','cik'])

# for index,record in cik_df.iterrows():
    
#     if pd.isna(record['cik']):
#         print("CIK not available")
#         continue
#     cik = str(int(record['cik']))
#     cik = '0'*(10-len(cik)) + cik
#     url = BASE_URL_CIK + 'CIK' + cik + '.json'
#     res = requests.get(url, headers={'user-agent':"interIIT krishna@inter.com",'Accept-Encoding':'gzip, deflate, br'})
#     try:
#         data = json.loads(res.text)
#     except:
#         print("error",record['name'])
#         continue
#     if not data.get('name'):
#         print("error",record['name'])
#         continue
#     name = data.get('name')
#     print(record['name'],name)

import os
import pandas as pd

PATH = "NLP Data"

folders = [name for name in os.listdir(PATH)]
companies = []

for folder in folders:
    company = folder.split('_')
    companies.append(company[0])
print(len(companies))
cik_df = pd.read_csv('result/res.csv', usecols=['name','cik'])
exluded = []
for index,record in cik_df.iterrows():
    if record['name'] not in companies:
        exluded.append(record['name'])

print(exluded)