from datetime import datetime
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import os
import random


BASE_URL_CIK = 'https://data.sec.gov/submissions/'
BASE_URL_FORM = 'https://www.sec.gov/Archives/edgar/data/'



cik_df = pd.read_csv('result/res.csv', usecols=['name','cik'])

company_list = ['NCINO INC', '30DC INC', 'ADEXA INC', 'ADVANT-E CORP', 'ALLDIGITAL HOLDINGS INC', 'AMERICAN SECURITY RES CORP', 'APPLIED VISUAL SCIENCES INC', 'B-SCADA INC', 'BUSYBOX.COM INC', 'CERIDIAN CORP', 'CIMETRIX INC', 'CLONE ALGO TECHNOLOGIES INC', 'CLOUDWARD INC', 'CODE REBEL CORP', 'COM GUARD.COM INC', 'DEALERADVANCE INC', 'E2OPEN INC', 'ELASTIC NETWORKS INC', 'ELCOM INTERNATIONAL INC', 'ENTERPRISE INFORMATICS INC', 'EZENIA INC', 'FANTASY ACES DAILY FANTASY', 'FRIENDFINDER NETWORKS INC', 'GRANDPARENTS.COM INC', 'GREEN POLKADOT BOX INC', 'HRSOFT INC', 'IBSG INTERNATIONAL INC', 'INFORMATION RESOURCES INC', 'INTEGRATED BUSINESS SYS &SVC', 'INTELLIGENT SYSTEM CORP', 'INTERMAP TECHNOLOGIES CORP', 'ISOCIALY INC', 'JDA SOFTWARE GROUP INC', 'KRONOS INC', 'LAWSON SOFTWARE INC', 'LIQUI-BOX CORP', 'LIQUID HOLDINGS GROUP INC', 'MAIL BOXES ETC', 'MEDALLIANCE INC', 'MONSTER ARTS', 'NEOMEDIA TECHNOLOGIES INC', 'NOTIFY TECHNOLOGY CORP', 'OMTOOL LTD', 'PRIMAL SOLUTIONS INC', 'PULSE EVOLUTION CORP', 'RAND WORLDWIDE INC', 'SCIENT INC', 'SIMTROL INC', 'SKYBOX INTL INC', 'SSI INVESTMENTS II LTD', 'TIBCO SOFTWARE INC', 'TMM INC', 'UNITRONIX CORP', 'VANCORD CAPITAL INC', 'VOYAGER DIGITAL LTD', 'VUBOTICS INC', 'XCELMOBILITY INC', 'ZOOM TELEPHONICS INC', 'ZOOMAWAY TRAVEL INC', 'BLAQCLOUDS INC', 'CHINA YANYUN YHU NTL ED GRP', 'FLEXSHARES IBOXX 3-YR TAR FD', 'FLEXSHARES IBOXX 5-YR TAR FD', 'ISHARES IBOXX HIGH YLD CP BD', 'ISHARES IBOXX INVST GR CP BD', 'LIVE MICROSYSTEMS INC', 'MEDIATECHNICS CORP', 'QUANTGATE SYSTEMS INC']
for index,record in cik_df.iterrows():


    if record['name'] not in company_list:
        continue

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
    print(len(scraped_indices))
    for j in scraped_indices:
        url =  BASE_URL_FORM + cik + '/'+ accession_no[j] + '.txt'
        req = requests.get(url, headers={'user-agent':"interIIT krishna@interIIT.com",'Accept-Encoding':'gzip, deflate, br'})
        file_content = req.text
        sub_str1 = file_content.find('<DOCUMENT>')
        sub_str2 = file_content.find('</DOCUMENT>')
        if len(file_content[sub_str1:sub_str2]) <10:
            write_data = file_content
        else:
            write_data = file_content[sub_str1:sub_str2]
        with open('test.txt','w') as f:
            f.write(write_data)
       
        with open("test.txt") as f:
            soup = BeautifulSoup(f.read(),'lxml')
            [s.extract() for s in soup(['style','table', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()

            try:
                os.makedirs("NLP Data/"+record['name']+"_"+cik)
            except:
                pass
            filename = "NLP Data/"+record['name']+"_"+cik +'/'+ form_type[j]+"_"+accepted_on[j][0:10]+".txt"
            while os.path.exists(filename):
                filename = "NLP Data/"+record['name']+"_"+cik +'/'+ form_type[j]+"_"+accepted_on[j][0:10]+"_"+str(random.randrange(1,10))+".txt"
            
            with open(os.path.join(filename),'x',encoding="utf-8") as m:
                m.write(visible_text)
    with open("logs.txt",'a') as n:
        n.writelines(record['name'])
        n.writelines('\n')

    print("End of ",record['name'])
