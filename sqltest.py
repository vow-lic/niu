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

conn = sqlite3.connect(app.config['DATABASE'])
cursor = conn.cursor()
'''values = cursor.execute('SELECT * FROM jianjiea WHERE NAME=?',[name])
print 'values git'
if values :
    print 'values take something'
else:
    print 'values is empty'
row = values.fetchall()
print row'''

cursor.execute('INSERT INTO jianjiea(name,habitat,bloodline,traits) VALUES (?,?,?,?)',\
               [name,habitat,bloodline,traits])
conn.commit()
values = cursor.execute('SELECT * FROM jianjiea WHERE NAME=?',[name])
print 'values git'
if values :
    print 'values take something'
else:
    print 'values is empty'
row = values.fetchall()
print row

cursor.close()
conn.close()
print 'over'