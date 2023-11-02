# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 19:22:39 2023

@author: USER
"""

import requests
from bs4 import BeautifulSoup
import db

url = "https://supertaste.tvbs.com.tw/food"

header = {
    'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

foods = requests.get(url,headers=header).text

soup = BeautifulSoup(foods,'html.parser')

allFoods = soup.find('div',class_='article__content')

a = allFoods.find_all('a')

for item in a:
    
    link = "https://supertaste.tvbs.com.tw/" + item.get('href')
    
    title = item.find('h3').text.strip()
    
    post_date = item.find('span').text.strip()
    
    photo_url = item.find('img').get('data-original')
    
    # 查詢來自product的資料表 where (條件) 欄位是food link要對應才能進入
    sql = "select * from food where link = '{}'".format(link)
    # 來自db.py裡面的cur
    db.cur.execute(sql)
    db.conn.commit()
        
    # no data
    if db.cur.rowcount == 0:
        
        sql = "insert into food(link, name, photo_url, create_date) value(%s, %s, %s, %s)"
        db.cur.execute(sql, [link, title, photo_url, post_date])
        db.conn.commit()
    
db.conn.close()









