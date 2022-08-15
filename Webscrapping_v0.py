# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 03:46:41 2022

@author: Balasubramanian P
"""


from bs4 import BeautifulSoup
from bs4 import element
import requests
from csv import writer
import os
import pandas as pd
import re

os.system('cls')
#Main Page url
url = f'https://www.stadt-koeln.de/leben-in-koeln/verkehr/parken/parkhaeuser/'

page = requests.get(url)

soup= BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())
parkPlatzTableList = soup.find_all('table',class_="data-table no-topheadtable table-striped datatable-head")
#print(parkPlatzTableList[0])
fname = "webscrapped.csv"
table = soup.find_all('table')
df = pd.read_html(str(table))
with open(fname,'w',encoding='utf8',newline='') as f:
     thewriter = writer(f)
     header = ['index','Parkhaus','Freie Plätz', 'Art','Adress','Betriebszeit','Weitere Datei']
     thewriter.writerow(header)
     df=pd.concat(df, axis=0, ignore_index=True)
     df.columns = ['Parkhaus','Art','Adress','Betriebszeit','Weitere Datei']
     df['Freie Plätz'] = df['Parkhaus'].str.extract('(\d+)', expand=True)
     df['Parkhaus'] = df['Parkhaus'].str.replace('(\d+)','')
     df.to_csv('web.csv') 
    



'''
with open(fname,'w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ['Parkhaus/Freie Plätz', 'Art','Adress','Betriebszeit','Weitere Datei']
    thewriter.writerow(header)
    row = []
    for each in parkPlatzTableList:
        parkPlaetz = soup.find('tbody')
        for i in parkPlaetz.find_all('tr'):
            for j in i.find_all('td'):
                row.append(j.text.replace('\n',''))
                #print(j.text)
    df = pd.DataFrame(row[1:], columns=['Parkhaus/Freie Plätz', 'Art','Adress','Betriebszeit','Weitere Datei'])            
    for each in df:
        thewriter.writerow(each)'''