import os, time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import datetime

data = pd.read_excel("web_scraping.xlsx")
chromedriver = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path = f'{chromedriver}')
driver.get("https://www.google.com/")

def googleForMayor(city, state):
    searchbox = driver.find_element_by_name('q')
    searchbox.clear()
    searchbox.send_keys('Who is the mayor of ' + city + ',' + ' ' + state)
    searchbox.send_keys(Keys.RETURN)
    try:
        quickAnswer = driver.find_element_by_class_name('FLP8od')
        return quickAnswer.text
    except:
        try: 
            quickAnswer = driver.find_element_by_css_selector('div.Z0LcW.XcVN5d.AZCkJd')
            return quickAnswer.text
        except:
            return np.nan

def sanitizeMayor(mayor):
    try:
        mayor = mayor.replace('Mayor ', '')
        return mayor
    except:
        return mayor

for index in range(0, len(data)):
    #if data['State'].iloc[index] == 'New York':
    city = data['City'].iloc[index]
    state = data['State'].iloc[index]
    mayor = googleForMayor(city, state)
    data['Mayor'].iloc[index] = sanitizeMayor(mayor)
    data['Checked'].iloc[index] = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    time.sleep(1)

data.to_excel('mayorOut.xlsx', index = False)