#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:44:11 2017

@author: lic
"""
import sqlite3
from flask import Flask
import os

#print os.path.join('static','testremove.txt')
#os.remove(os.path.join('static','testremove.txt'))
#print 'remove over'
app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'Niupinz.db')

values = None
name = u'九龙牦牛'
data = []
Map = [['ID',0],[u'品种名称',0],[u'品种图片',1],[u'产地与分布',0],[u'品种形成',0],[u'体型外貌',0],[u'生长发育',0],[u'生产性能',0],[u'繁殖性能',0],[u'杂交效果',0],['适应性能',0],[u'评价与展望',0]]
conn = sqlite3.connect(app.config['DATABASE'])
cursor = conn.cursor()

'''cursor.execute('CREATE TABLE "jianjie" \
               ("ID" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,\
               "NAME" NVARCHAR(5) NOT NULL ,\
               "PICTURE" TEXT,\
               "CDFB" TEXT,\
               "PZXC" TEXT,\
               "TXWM" TEXT,\
               "SZFY" TEXT,\
               "SCXN" TEXT,\
               "FZXN" TEXT,\
               "ZJXG" TEXT,\
               "SYXN" TEXT,\
               "PJYZW" TEXT);')'''

'''cursor.execute('INSERT INTO jianjie(NAME,PICTURE) VALUES (?,?)',\
               ['NAME','PICTURE'])'''

values = cursor.execute('SELECT * FROM jianjie WHERE NAME=?',[name])
print 'values git'
if values :
    print 'values take something'
else:
    print 'values is empty'
row = values.fetchall()[0]
print len(row)
print row
print len(Map)
data = Map
for i in range(len(Map)):
    data[i].append(row[i])

print data
#names = cursor.execute('SELECT NAME FROM jianjie')
#NAMES = names.fetchall()
#print 'NAMES',NAMES

conn.commit()


cursor.close()
conn.close()
print 'over'