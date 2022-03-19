from datetime import datetime
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import os
import random


BASE_URL_CIK = 'https://data.sec.gov/submissions/'

cik_df = pd.read_csv('result/res.csv', usecols=['name','cik'])

df = pd.DataFrame(columns=['cik','form','date','accession_no'])

for index,record in cik_df.iterrows():

    if pd.isna(record['cik']):
        print("CIK not available")
        continue
    cik = str(int(record['cik']))
    cik = '0'*(10-len(cik)) + cik
    url = BASE_URL_CIK + 'CIK' + cik + '.json'
    
    url = BASE_URL_CIK + 'CIK' + cik + '.json'
    res = requests.get(url, headers={'user-agent':"interIIT krishna@interIIT.com",'Accept-Encoding':'gzip, deflate, br'})
    try:
        data = json.loads(res.text)
    except:
        print("error",record['name'])
        continue
    recent_filings = data["filings"]['recent']
    accession_no = recent_filings['accessionNumber']
    accepted_on =  recent_filings['acceptanceDateTime'] 
    form_type = recent_filings['form']
    
    scraped_indices = []

    for i in range(len(accepted_on)):
        sub_date = datetime.strptime(accepted_on[i],"%Y-%m-%dT%H:%M:%S.%fZ")
        if sub_date<datetime(2017,1,1,0,0):
            break
        if form_type[i]=='10-K' or form_type[i]=='10-Q':
            scraped_indices.append(i)
    
    for i in scraped_indices:
        entry = {
            "cik":cik,
            "form":form_type[i],
            "date":accepted_on[i],
            "accession_no":accession_no[i]
        }
        df = df.append(entry,ignore_index=True)

df.to_csv("accession.csv")