#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:44:11 2017

@author: lic
"""
import sqlite3
import os
from flask import Flask

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'niupinzhong.db')

values = None


#name = u'蜀宣花牛'
#name = 'safasdf'
name = 'jiulong'
habitat = 'ganzi'
bloodline = 'yak'
traits = None
img=None
conn = sqlite3.connect(app.config['DATABASE'])
cursor = conn.cursor()
'''values = cursor.execute('SELECT * FROM jianjie WHERE NAME=?',[name])
print 'values git'
if values :
    print 'values take something'
else:
    print 'values is empty'
row = values.fetchall()
print row'''

cursor.execute('CREATE TABLE "jianjie" \
               ("NAME" NVARCHAR(5) NOT NULL ,\
               "HABITAT" NVARCHAR(20),\
               "BLOODLINE" NVARCHAR(40),\
               "TRAITS" NVARCHAR(90),\
               "IMG" NVARCHAR(20),\
               "SOURCE" NVARCHAR(90),\
               "ID" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE);')
'''cursor.execute('INSERT INTO jianjie(name,habitat,bloodline,traits,img) VALUES (?,?,?,?,?)',\
               [name,habitat,bloodline,traits,img])'''

conn.commit()


cursor.close()
conn.close()
print 'over'