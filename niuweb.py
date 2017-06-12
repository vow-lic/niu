#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:52:45 2017

@author: lic
"""
import os
from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'apmfeuasdfghjklzxcvbnm'
app.config['DATABASE'] = os.path.join(app.root_path, 'niupinzhong.db')

class SeachForm(FlaskForm):
    name = StringField(u'xxx', validators=[Required()])
    submit = SubmitField(u'提交')

@app.route('/',methods=['POST','GET'])
def index(): 
    name = None
    HABITAT = None
    BLOODLINE = None
    TRAITS = None
    form = SeachForm()
    print 'form : {}'.format(form)
    if request.method == 'POST':
        print '1\n\n'
        name = form.name.data
        print name
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        values = cursor.execute('SELECT * FROM jianjiea WHERE NAME=?',[request.form['name']])
        for row in values:
            print row[:]
            NAME = row[1]
            HABITAT = row[2]
            BLOODLINE = row[3]
            TRAITS = row[4]
            cursor.close()
            conn.close()
#        form.name.data = ''

            return render_template('index.html',form=form,name=NAME,habitat=HABITAT,\
                           bloodline=BLOODLINE,traits=TRAITS)
    else:
        print '2\n\n'
        
        return render_template('index.html',form=form)
    
if __name__ == '__main__':
    app.run(debug=True)