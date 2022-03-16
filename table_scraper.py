from datetime import datetime
import json
import os
import random
from turtle import st
import pandas as pd
import requests
from bs4 import BeautifulSoup

extraction = ["Risk Factors","Legal Proceedings","Management’s Discussion and Analysis of Financial Condition and Results of Operations",'Quantitative and Qualitative Disclosures About Market Risk']
next_item = ["Unresolved Staff Comments","Mine Safety Disclosures","Quantitative and Qualitative Disclosures About Market Risk",'Financial Statements and Supplementary Data']

BASE_URL_CIK = 'https://data.sec.gov/submissions/'
BASE_URL_FORM = 'https://www.sec.gov/Archives/edgar/data/'
cik_df = pd.read_csv('result/res.csv', usecols=['name','cik'])


start = False

for index,record in cik_df.iterrows():
    if record['name']=='IMAGEWARE SYSTEMS INC':
        start = True
    if not start:
        continue
    if pd.isna(record['cik']):
        print("CIK not available")
        continue
    cik = str(int(record['cik']))
    cik = '0'*(10-len(cik)) + cik
    url = BASE_URL_CIK + 'CIK' + cik + '.json'
    res = requests.get(url, headers={'user-agent':"interIIT krishna@inter.com",'Accept-Encoding':'gzip, deflate, br'})
    try:
        data = json.loads(res.text)
    except:
        continue
    recent_filings = data["filings"]['recent']
    accession = recent_filings['accessionNumber']
    accepted_on =  recent_filings['acceptanceDateTime'] 
    form_type = recent_filings['form']
    
    scraped_indices = []
    for i in range(len(accepted_on)):
        sub_date = datetime.strptime(accepted_on[i],"%Y-%m-%dT%H:%M:%S.%fZ")
        if sub_date<datetime(2017,1,1,0,0):
            break
        if form_type[i]=='10-K':
            scraped_indices.append(i)
    
    for k in scraped_indices:
        accession_no = accession[k]
        
        
        url =  BASE_URL_FORM + cik + '/'+ accession_no + '.txt'
        req = requests.get(url, headers={'user-agent':"interIIT krishna@inter.com",'Accept-Encoding':'gzip, deflate, br'})
        
        file_content = req.text
        sub_str1 = file_content.find('<DOCUMENT>')
        sub_str2 = file_content.find('</DOCUMENT>')
        if len(file_content[sub_str1:sub_str2]) <10:
            write_data = file_content
        else:
            write_data = file_content[sub_str1:sub_str2]
        with open('test.txt','w',encoding="utf-8") as f:
            f.write(write_data)
        with open("test.txt") as f:
            soup = BeautifulSoup(f.read(),'lxml')
        
        all_divs = soup.findAll('div')
        found_table = False
        for i in range(1,len(all_divs)-1):
            content_line = all_divs[i-1].get_text()
            if content_line.upper()=="TABLE OF CONTENTS":
                table = all_divs[i-1].find_next('table')
                if 'RISK FACTORS' in table.get_text().upper():
                    found_table = True
                    break
        if not found_table:
            all_divs = soup.findAll('p')
            for i in range(1,len(all_divs)-1):
                content_line = all_divs[i-1].get_text()
                if content_line.upper()=="TABLE OF CONTENTS":
                    table = all_divs[i-1].find_next('table')
                    if 'RISK FACTORS' in table.get_text().upper():
                        found_table = True
                        break
                    found_table = True
                    break
        
        text = ""

        for section in extraction:
            try:
                all_rows = table.find_all("tr")
                for row in all_rows:
                    if section.upper() in row.get_text().upper():
                        cols = row.find_all("a")
                        for col in cols:
                            if section.upper() == col.get_text().upper():
                                
                                item8 = col['href']
                                item8 = item8[1:]
                        break
                        
            except:
                continue
            try:
                item = soup.find(id=item8)
            except: 
                continue
            try:
                divs = item.find_all_next('div')
                ps = item.find_all_next('p')
                divs = divs + ps
            except:
                item = soup.find('a',{'name':item8})
                try:
                    divs = item.find_all_next('div')
                    ps = item.find_all_next('p')
                    divs = divs + ps
                except:
                    print("error",cik,accession_no)
                    continue
            
            for div in divs:
                div_tables = div.find_all("table")
                if len(div_tables)>0:
                    continue
                line = div.get_text()
                if next_item[extraction.index(section)].upper() in line.upper() :
                    break
                
                if 'TABLE OF CONTENTS' in line.upper():
                    continue
                try:
                    if int(line):
                        continue
                except:
                    pass

                text = text + " " + line


        # section = "Financial Statements and Supplementary Data"
        # all_rows = table.find_all("tr")
        # for row in all_rows:
        #     if section in row.get_text():
        #         cols = row.find_all("a")
        #         for col in cols:
        #             if section in col.get_text():
        #                 item8 = col['href']
        #                 item8 = item8[1:]
        #         break
        # item = soup.find('div',id=item8)
        # section = "Notes to Consolidated Financial Statements"
        # try:
        #     table2 = item.find_next('table')
        #     all_rows = table2.find_all("tr")
        # except:
        #     continue

        # for row in all_rows:
        #     if section in row.get_text():
        #         cols = row.find_all("a")
        #         for col in cols:
        #             if section in col.get_text():
        #                 item = col['href']
        #                 item = item[1:]
        #         break

        # item = soup.find('div',id=item)
        # divs = item.find_all_next('div')
        
        # for div in divs:
        #     div_tables = div.find_all("table")
        #     if len(div_tables)>0:
        #         continue
            
        #     line = div.get_text()
        #     if 'REPORT OF INDEPENDENT REGISTERED PUBLIC ACCOUNTING FIRM' in line.upper() and section.upper() not in line.upper():
        #         break
        #     if 'Table of Contents' in line:
        #         continue
        #     try:
        #         if int(line):
        #             continue
        #     except:
        #         pass
        #     text = text + " " + line

        try:
            os.makedirs("Sentiment/"+record['name']+"_"+cik)
        except:
            pass
        filename = "Sentiment/"+record['name']+"_"+cik +'/'+ form_type[k]+"_"+accepted_on[k][0:10]+".txt"
        while os.path.exists(filename):
            filename = "Sentiment/"+record['name'] +"_"+cik +'/'+ form_type[k]+"_"+accepted_on[k][0:10]+"_"+str(random.randrange(1,10))+".txt"
        with open(filename,'x',encoding="utf-8") as m:
            m.write(text)
        
        
    

