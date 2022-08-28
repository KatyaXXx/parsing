# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 16:49:11 2022

"""

import requests
from bs4 import BeautifulSoup



#**********************************************************

url_all = []
url3 = "https://fix-price.ru/catalog/"
url_all.append(url3)

#**********************************************************"""

r= requests.get(url3)
soup = BeautifulSoup(r.text,"lxml")
try:
   pages = soup.findAll('li', class_='paging__item')
except Exception:
   pages=0
if pages!=0:
    for i in range(2,int(pages[-1].text)+1):
        url_all.append(url3+"?PAGEN_1="+str(i))
    
        
        
#Достаем атрибуты

data=[]

for item in url_all:
    r= requests.get(item)
    soup = BeautifulSoup(r.text,"lxml")
#**********************************************************
    #Достаем кол-во страниц  
    for item in soup.findAll('div', class_='product-card product-card--md'):
        SKU = item.find('a', class_='product-card__title').text
        href = "https://fix-price.ru"+item.find('a', class_='product-card__title').get('href')
        try:
            price = item.find('span', class_='badge-price-value badge-price-value--lg').get('data-price')
        except Exception:
            try:
                price = item.find('span', class_='badge-price-value badge-price-value--md').get('data-price')
            except Exception:
                try:
                    price = item.find('span', class_='badge-price-value badge-price-value--sm').get('data-price') 
                except Exception:
                        price = item.find('span', class_='badge-price-value badge-price-value--mdn').get('data-price')
   
        while "  " in SKU:
            SKU= SKU.replace("  ", " ")
        price = price.replace('.',',')
        data.append([SKU, price,href])
    
   


import pandas as pd
header=['name','price','href']
df = pd.DataFrame(data,columns=header)
df.to_excel("fix_price_Parse.xlsx",encoding='utf16')