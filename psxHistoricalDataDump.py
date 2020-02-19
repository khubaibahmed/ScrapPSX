# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 12:58:18 2019

@author: KhubaibAhmed
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
chromedriver = "chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.psx.com.pk/psx/resources-and-tools/listings/listed-companies")

select = Select(driver.find_element_by_id("sector"))
options = select.options
listComp = pd.DataFrame()
for idx, val in enumerate(options):
    if idx == 0 or val.text == "Future contracts":
        continue
    select.select_by_index(idx)
    time.sleep(2)
    df = pd.read_html(driver.page_source)[0]
    print(idx, len(df), val.text)
    df['Sector'] = val.text
    listComp=listComp.append(df)

driver.close()
listComp = listComp.reset_index(drop=True)    
listComp.to_csv("psxCompnayListOffWeb.csv")

driver = webdriver.Chrome(chromedriver)
driver.get("https://dps.psx.com.pk/historical")

psxhist= pd.DataFrame()
selectM = Select(driver.find_element_by_xpath("//div[@class='dropdown historical__month']//select[@class='dropdown__select']"))
selectY = Select(driver.find_element_by_xpath("//div[@class='dropdown historical__year']//select[@class='dropdown__select']"))
submit = driver.find_element_by_id('historicalSymbolBtn')
textField = driver.find_element_by_id("historicalSymbolSearch")
# Iterate over Company List 
for index, lrow in listComp.iterrows():
    print(lrow['Symbols'])
    textField.send_keys(lrow['Symbols'])

    
    optionsM = selectM.options
    optionsY = selectY.options
    listComp = pd.DataFrame()
    # Selecy Year
    for idy, valY in enumerate(optionsY):
        if idy == 0 or idy ==1:
            continue
        selectY.select_by_index(idy)
        #Select Month
        for idm, valM in enumerate(optionsM):
            if idm == 0:
                continue
            selectM.select_by_index(idm)

            submit.click()
            time.sleep(5)
            try:     
                df = pd.read_html(driver.page_source)[0]
            except Exception as e:
                print(e)
            print(valY.text,"  ",valM.text," ", len(df))
            if len(df) == 1:
                continue
            psxhist=psxhist.append(df)