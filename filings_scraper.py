from datetime import datetime
import pandas
import requests
import json
from bs4 import BeautifulSoup
import os
import random


BASE_URL_CIK = 'https://data.sec.gov/submissions/'
BASE_URL_FORM = 'https://www.sec.gov/Archives/edgar/data/'

companies_list = ['VARONIS SYSTEMS INC']

cik_df = pandas.read_csv('csv/res.csv', usecols=['name','cik'])


for company in companies_list:
    [record] = cik_df.index[cik_df['name'] == company]
    cik = str(int(cik_df.at[record,'cik']))
    if pandas.isna(cik):
        print("CIK not available")
        continue
    cik = '0'*(10-len(cik)) + cik
    
    url = BASE_URL_CIK + 'CIK' + cik + '.json'
    res = requests.get(url, headers={'user-agent':"interIIT krishna@interIIT.com",'Accept-Encoding':'gzip, deflate, br'})
    data = json.loads(res.text)
    
    recent_filings = data["filings"]['recent']
    accession_no = recent_filings['accessionNumber']
    accepted_on =  recent_filings['acceptanceDateTime'] 
    form_type = recent_filings['form']
    
    scraped_indices = []
    
    for i in range(len(accepted_on)):
        sub_date = datetime.strptime(accepted_on[i],"%Y-%m-%dT%H:%M:%S.%fZ")
        if sub_date<datetime(2020,1,1,0,0):
            break
        if form_type[i]=='8-K' or form_type[i]=='10-K' or form_type[i]=='10-Q':
            scraped_indices.append(i)
    
    for j in scraped_indices:
        url =  BASE_URL_FORM + cik + '/'+ accession_no[j] + '.txt'
        req = requests.get(url, headers={'user-agent':"interIIT krishna@interIIT.com",'Accept-Encoding':'gzip, deflate, br'})
        file_content = req.text
        sub_str1 = file_content.find('<XBRL>')
        sub_str2 = file_content.find('</XBRL>')
        if len(file_content[sub_str1:sub_str2]) <10:
            write_data = file_content
        else:
            write_data = file_content[sub_str1:sub_str2]
        with open('test.txt','w') as f:
            f.write(write_data)
       
        with open("test.txt") as f:
            soup = BeautifulSoup(f.read(),'lxml')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()

            try:
                os.makedirs("NLP Data/"+company)
            except:
                pass
            filename = "NLP Data/"+company +'/'+ form_type[j]+"_"+accepted_on[j][0:10]+".txt"
            while os.path.exists(filename):
                filename = "NLP Data/"+company +'/'+ form_type[j]+"_"+accepted_on[j][0:10]+"_"+str(random.randrange(1,10))+".txt"
            clean_index = visible_text.find("UNITED")
            if len(visible_text[clean_index:])<10:
                print("--------------------------------------")
                print(clean_index)
                print(url)
                print("--------------------------------------")
            with open(os.path.join(filename),'x',encoding="utf-8") as m:
                m.write(visible_text[clean_index:])

    print("End of ",company)
