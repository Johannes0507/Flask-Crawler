# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 00:51:54 2023

@author: KeithLee
"""

import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1234567890',
    database = 'myweb',
    auth_plugin = 'mysql_native_password'
        )

cur = conn.cursor(buffered=True)