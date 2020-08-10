import os, time
import re
import pandas as pd
import numpy as np

data = pd.read_excel("mayorOut.xlsx")
k = 0

for index, row in data.iterrows():

    mayorString = data['Mayor'].iloc[index]
    if type(mayorString) != type('string here'):
        continue
    if '??? FULL NAME' in str(mayorString):
        mayorArray = re.split(re.escape('???'), mayorString)
        data['Possible Extracted Mayor Name'].iloc[index] = mayorArray[0]
        continue
    if 'Missing: mayor' in str(mayorString):
        continue
    if 'Must include: mayor' in str(mayorString):
        continue

    mayorArray = re.split(' |_|-|, |\n', mayorString)

    for i in range(len(mayorArray)):
        if mayorArray[i] == 'Mayor:' or mayorArray[i] == 'mayor:':

                possibleName = []
                possibleName.append(mayorArray[i + 1])
                possibleName.append(mayorArray[i + 2])
                
                if '.' in mayorArray[i + 2]:
                    if len(mayorArray[i + 2]) <= 2:
                        possibleName.append(mayorArray[i + 3])
        else: 
            if mayorArray[i] == 'mayor' or mayorArray[i] == 'Mayor':
                
                possibleName = []
                possibleName.append(mayorArray[i + 1])
                possibleName.append(mayorArray[i + 2])

                if '.' in mayorArray[i + 2]:
                    if len(mayorArray[i + 2]) <= 2:
                        possibleName.append(mayorArray[i + 3])

    data['Possible Extracted Mayor Name'].iloc[index] = ' '.join(possibleName)
    possibleMayorArray = re.split(' ', data['Possible Extracted Mayor Name'].iloc[index])

    if index == 30:
        print('pause')
    for l in range(len(possibleMayorArray)):
        if '.' in possibleMayorArray[l]:
            if len(possibleMayorArray[l]) >= 3:
                possibleMayorArray[l].replace('.', '')
        
    k = k + 1
    if k >= 100:
        data.to_excel('mayorOutv2.xlsx', index = False)
        break