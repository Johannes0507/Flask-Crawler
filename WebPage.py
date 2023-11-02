# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:16:04 2023

@author: KeithLee
"""

from flask import Flask, render_template, request, redirect, url_for
from GetNews import GetNews
import db
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def HomePage():
    
    allNews = GetNews()[:4]
    
    sql = "select * from product order by id desc limit 4"
    db.cur.execute(sql)
    allGoods = db.cur.fetchall()
    
    sql = "select name, photo_url, link, create_date from food order by photo_url limit 4"
    db.cur.execute(sql)
    db.conn.commit()
    allFood = db.cur.fetchall()
    
    return render_template('index.html', **locals())


@app.route('/news')
def news():
    
    allNews = GetNews()
    # **意思是可以讓字典變數裡key相對應function裡面的key值 
    # locals() 它返回當前作用域中的所有變數和對應的值的字典
    # 這包括局部變數、函數參數以及全局變數 
    return render_template('news.html', **locals())


@app.route('/products')
def Product():
    # 通常部會用* because the data may be too large
    sql = "select * from product order by id desc"
    
    db.cur.execute(sql) 
    
    # 把檢視內容從網頁緩衝區全部呼叫出來
    allGoods = db.cur.fetchall()
    
    return render_template('products.html', **locals())


@app.route('/food')
def Food():
    sql = "select name, link, photo_url, create_date from food order by photo_url"
    db.cur.execute(sql)
    db.conn.commit()
    allFood = db.cur.fetchall()
    
    return render_template('Food.html', **locals())


@app.route('/contact')
def ContactUS():
    return render_template('contact.html', **locals())


@app.route('/addcontact', methods=['POST'])
def Contact_Form():
    if request.method == 'POST':
        title = request.form.get('title')
        usename = request.form.get('nickname') 
        email = request.form.get('email')        
        content = request.form.get('advice')
        date = datetime.today().strftime('%Y-%m-%d')
        
        sql = "insert into contact(name, title, email, content, create_date) value('{}', '{}', '{}', '{}', '{}')".format(usename, title, email, content, date)
        db.cur.execute(sql)
        db.conn.commit()
        
    return redirect(url_for('ContactUS'))
    

app.run(debug=True)
