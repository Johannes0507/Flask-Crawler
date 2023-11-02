# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 19:41:01 2023

@author: USER
"""


import requests
import json
import time
import datetime
import db

url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results'

header = {
    'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    
param = {

    'q':'可口可樂',
'page':'1',
'sort':'sale/dc'    
    
    } 

for i in range(1,6):
    
    param['page'] = str(i)

    pchome = requests.get(url,headers=header,params=param).text
    
    pchome = json.loads(pchome)
    
    allgoods = pchome['prods']
    
    for item in allgoods:
        img = 'https://cs-c.ecimg.tw/' +item['picB']
        name = item['name']
        info = item['describe']
        price = item['price']
        link = "https://24h.pchome.com.tw/prod/" + item['Id']
    
        
        # 查詢來自product的資料表 where (條件) 欄位是Pchome link要對應才能進入 (因為每一個link都是獨一無二的所以可以設立這個條件)
        sql = "select * from product where plateform = 'Pchome' and link = '{}'".format(link)
        # 來自db.py裡面的cur 
        db.cur.execute(sql)
        db.conn.commit()
        
        # rowcount 筆數
        if db.cur.rowcount == 0:
    
            today = datetime.datetime.today()
            # Y -> 年的四個數字 y -> 年的兩個數字
            now = today.strftime('%Y-%m-%d')
            # 插入mysql > myweb table product 裡面相對應欄位
            sql = "insert into product(plateform, title, photo_url, link, price, onsale, create_date) values(%s,%s,%s,%s,%s,%s,%s)"
            
            db.cur.execute(sql, ['Pchome', name, img, link, price, price, now])    
            # 提交
            db.conn.commit()
            

    time.sleep(2)
# 關閉
db.conn.close()



  