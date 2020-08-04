import os, time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import datetime

i = 0

data = pd.read_excel("master_sheet.xlsx")
chromedriver = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path = f'{chromedriver}')
driver.get("https://www.google.com/")
lastMayor = ''

def googleForMayor(city, state, category):
    searchbox = driver.find_element_by_name('q')
    searchbox.clear()
    searchbox.send_keys('Who is the mayor of ' + city + ' ' + category +  ',' + ' ' + state)
    searchbox.send_keys(Keys.RETURN)
    try:
        quickAnswer = driver.find_element_by_class_name('FLP8od') #find quick answer if it is in standard text format
        return quickAnswer.text + ' ??? FULL NAME'
    except:
        try: 
            quickAnswer = driver.find_element_by_css_selector('div.Z0LcW.XcVN5d.AZCkJd') #find quick answer if it is in standard text format
            return quickAnswer.text + ' ??? FULL NAME'
        except:
            try:
                quickAnswer = driver.find_element_by_class_name('webanswers-webanswers_table__webanswers-table') #find quick answer if it is in a table format
                return quickAnswer.text + ' ??? TABLE FORMAT'
            except:
                try:
                    topResultDescription = driver.find_elements_by_class_name('g') #return the top web result page description. Excludes wikipedia results
                    if 'wikipedia' in topResultDescription[0].text:
                        return topResultDescription[1].text
                    else:
                        return topResultDescription[0].text + ' ??? WEBPAGE DESCRIPTION'
                except:
                    return np.nan

def sanitizeMayor(mayor):
    try:
        mayor = mayor.replace('Mayor ', '')
        return mayor
    except:
        return mayor

for index, row in data.iterrows():
    city = data['Name'].iloc[index]
    test = data['Mayor'].iloc[index]
    state = data['State'].iloc[index]
    category = data['Type'].iloc[index]
    mayor = googleForMayor(city, state, category)
    if 'FULL NAME' in mayor:
        mayor = sanitizeMayor(mayor)
    if mayor == lastMayor:
        mayor = np.nan
    data['Mayor'].iloc[index] = mayor
    time.sleep(1)
    lastMayor = data['Mayor'].iloc[index]
    if i >= 1000:
        data.to_excel('mayorOut.xlsx', index = False)
        i = 0
    i =  i + 1
    print(i)

data.to_excel('mayorOut.xlsx', index = False)