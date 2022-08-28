# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 16:49:11 2022

"""

import requests
from bs4 import BeautifulSoup



#**********************************************************
#Достаем "дерево"
url_all = []
url3 = "https://spb-mineralnaya.svetoforonline.ru/"

r= requests.get(url3)
soup_tree = BeautifulSoup(r.text,"lxml")


for item in soup_tree.findAll('h2', class_='mainh2'):
    tree = item.find('a').get('href')
    url_all.append("https://spb-mineralnaya.svetoforonline.ru/"+tree)
#**********************************************************


        
#Достаем атрибуты

data=[]

for item in url_all:
    r= requests.get(item)
    soup = BeautifulSoup(r.text,"lxml")
    try:
        pages=soup.find('td', class_='paging').findAll('a')
        flag=pages[-3].text
    except Exception: 
        flag=0
    
    if flag==0:
        for item in soup.findAll('div', class_='grid_3'):
            SKU = item.find('div', class_='name').find('a').text
            #print(SKU)
            href = "https://spb-mineralnaya.svetoforonline.ru"+item.find('div', class_='name').find('a').get('href')
            price = item.find('div', class_='price').find('big').text+item.find('div', class_='price').find('sup').text
            while "  " in SKU:
                SKU= SKU.replace("  ", " ")
            price = price.replace('.',',')
            data.append([SKU, price,href])
            
    else:
        for i in range(1, int(flag)+1):
            print(item)
            hr= item + "page"+ str(i) +".htm"
            print(hr)
            t= requests.get(hr)
            soupt = BeautifulSoup(t.text,"lxml")
            for item_n in soupt.findAll('div', class_='grid_3'):
                SKU = item_n.find('div', class_='name').find('a').text
                #print(SKU)
                href = "https://spb-mineralnaya.svetoforonline.ru"+item_n.find('div', class_='name').find('a').get('href')
                price = item_n.find('div', class_='price').find('big').text+item_n.find('div', class_='price').find('sup').text
                while "  " in SKU:
                    SKU= SKU.replace("  ", " ")
                price = price.replace('.',',')
                data.append([SKU, price,href])

   


import pandas as pd
header=['name','price','href']
df = pd.DataFrame(data,columns=header)
df.to_excel("Svetofor_Parse.xlsx",encoding='utf16')