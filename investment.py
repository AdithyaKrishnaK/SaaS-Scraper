
import requests
import json
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://www.investing.com/'
BASE_URL_CIK = 'https://data.sec.gov/submissions/'

from selenium.webdriver.common.keys import Keys

PATH = r'D:\Utilities\chromedriver'
driver = webdriver.Chrome(PATH)

driver.get(URL)
time.sleep(10)
cik_df = pd.read_csv('result/res.csv', usecols=['name','cik'])


start = False

# for index,record in cik_df.iterrows():
    # if pd.isna(record['cik']):
    #     print("CIK not available")
    #     continue
    # cik = str(int(record['cik']))
    # cik = '0'*(10-len(cik)) + cik
    # url = BASE_URL_CIK + 'CIK' + cik + '.json'
    # res = requests.get(url, headers={'user-agent':"interIIT krishna@inter.com",'Accept-Encoding':'gzip, deflate, br'})
    # try:
    #     data = json.loads(res.text)
    # except:
    #     print("error",record['name'])
    #     continue
    # tickers = data.get('tickers')
    # for tick in tickers:
search_box = driver.find_element_by_xpath("//input[@class='searchText arial_12 lightgrayFont js-main-search-bar']")
search_box.send_keys("TWLO")
time.sleep(5)
search_box = driver.find_element_by_xpath("//a[@class='row js-quote-row-template js-quote-item']")
if "NASDAQ" or "NYSE" in search_box.text:
    search_box.click()
    time.sleep(5)
    url = driver.current_url
    print(url)
    time.sleep(5)
    driver.get(url+"-ratios")
    time.sleep(5)
    table = driver.find_element_by_id('rrTable')
    links= driver.find_elements_by_tag_name('tr')
    for link in links:
        cols = link.find_elements_by_tag_name('td')
        for col in cols:
            print(col.text)
