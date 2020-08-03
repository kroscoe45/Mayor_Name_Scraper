import os, time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import datetime

data = pd.read_excel("master_sheet.xlsx")
chromedriver = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path = f'{chromedriver}')
driver.get("https://www.google.com/")

def googleForMayor(city, state, category):
    searchbox = driver.find_element_by_name('q')
    searchbox.clear()
    searchbox.send_keys('Who is the mayor of ' + city + ' ' + category +  ',' + ' ' + state)
    searchbox.send_keys(Keys.RETURN)
    try:
        quickAnswer = driver.find_element_by_class_name('FLP8od')
        return quickAnswer.text
    except:
        try: 
            quickAnswer = driver.find_element_by_css_selector('div.Z0LcW.XcVN5d.AZCkJd')
            return quickAnswer.text
        except:
            try 
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
    data['Mayor'].iloc[index] = sanitizeMayor(mayor)
    if data['Mayor'].iloc[index] == lastMayor:
        data['Mayor'].iloc[index] = np.nan
    time.sleep(1)
    lastMayor = data['Mayor'].iloc[index]

data.to_excel('mayorOut.xlsx', index = False)