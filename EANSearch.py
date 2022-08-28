# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 20:25:53 2022

"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

EAN_data = pd.read_csv('data.csv',delimiter=',',names=['EAN', 'smthElse'])

names=[]
for item in EAN_data['EAN']:
    """"listex.info"""
    try:
        url = "https://listex.info/search/?q="+str(item)+"&type=goods"
        r= requests.get(url)
        soup= BeautifulSoup(r.text,"lxml")
        listex = soup.find('img', class_='products-slider__item__image img-responsive').get('alt')
    except Exception:
        listex =''   

    try:
        url = "https://barcode-list.ru/barcode/RU/barcode-"+str(item)+"/Поиск.htm"
        r= requests.get(url)
        soup= BeautifulSoup(r.text,"lxml")
        barcode_list = soup.find('h1', class_='pageTitle').text
        barcode_list=barcode_list.partition(' - Штрих')[0]
    except Exception:
       barcode_list=''    
        
    try:
         url = "https://www.ozon.ru/search/?text="+str(item)+"&from_global=true"
         r= requests.get(url)
         soup= BeautifulSoup(r.text,"lxml")
         ozone = soup.find('span', class_='cy2 yc2 cy3 y4c tsBodyL i1k').text
    except Exception:
        ozone=''  
    try:
         url = "https://www.google.com/search?q=%D1%81%D0%B1%D0%B5%D1%80%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82+"+str(item)
         r= requests.get(url)
         soup= BeautifulSoup(r.text,"lxml")
         sbermarket = soup.find('div', class_='BNeawe vvjwJb AP7Wnd').text
         sbermarket=sbermarket.partition('- ')[0]
    except Exception:
        sbermarket='' 
    try:
         url = "https://www.google.com/search?q=ean+"+str(item)
         r= requests.get(url)
         soup= BeautifulSoup(r.text,"lxml")
         google = soup.find('div', class_='BNeawe vvjwJb AP7Wnd').text
    except Exception:
        google=''         
    names.append([item,listex,barcode_list,ozone,sbermarket,google])

header=['EAN','listex','barcode_list','ozone','sbermarket','google']
df = pd.DataFrame(names,columns=header)

df.to_excel("EAN_data.xlsx",encoding='utf8')