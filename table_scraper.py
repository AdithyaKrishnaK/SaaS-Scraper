import pandas as pd
import requests
from bs4 import BeautifulSoup

def custom_parser(table_data):
    rows = table_data.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            pass



BASE_URL_FORM = 'https://www.sec.gov/Archives/edgar/data/'
cik = '0001045810'#'796343'
accession_no = '0001045810-21-000010' #'0000796343-22-000032'
url =  BASE_URL_FORM + cik + '/'+ accession_no + '.txt'

req = requests.get(url, headers={'user-agent':"interIIT krishna@interIIT.com",'Accept-Encoding':'gzip, deflate, br'})
file_content = req.text
sub_str1 = file_content.find('<XBRL>')
sub_str2 = file_content.find('</XBRL>')
if len(file_content[sub_str1:sub_str2]) <10:
    write_data = file_content
else:
    write_data = file_content[sub_str1:sub_str2]
with open('test.txt','w',encoding="utf-8") as f:
    f.write(write_data)
with open("test.txt") as f:
    soup = BeautifulSoup(f.read(),'lxml')
all_divs = soup.findAll('div')
for i in range(1,len(all_divs)-1):
    if(all_divs[i-1].get_text()=="TABLE OF CONTENTS"):
        table = all_divs[i-1].find_next('table')
        break



try:
    all_rows = table.find_all("tr")
    for row in all_rows:
        if 'Item 8.' in row.get_text():
            cols = row.find_all("a")
            for col in cols:
                if 'Financial Statements and Supplementary Data' in col.get_text():
                    item8 = col['href']
                    item8 = item8[1:]
            break

except:
    print('item 8 not found')
    quit()

# try:
item = soup.find('div',id=item8)
item_table = item.find_all_next('table')
df = pd.read_html(str(item_table))
df[1].to_csv("assets1.csv")