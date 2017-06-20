#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:52:45 2017

@author: lic
"""
import os
import sys
import sqlite3
from flask import Flask,render_template,request,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask.ext.script import Manager

reload(sys)  
sys.setdefaultencoding('utf8') 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'apmfeuasdfghjklzxcvbnm'
app.config['DATABASE'] = os.path.join(app.root_path, 'niupinzhong.db')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path,'static')
ALLOWED_EXTENSIONS = set(['jpg','png'])
bootstrap = Bootstrap(app)
manager = Manager(app)

class SeachForm(FlaskForm):
    name = StringField(u'请输入您要查询的品种', validators=[Required()])
    submit = SubmitField(u'提交')

class AddForm(FlaskForm):
    name = StringField(u'品种名称',validators=[Required()])
    habitat = StringField(u'产地',validators=[Required()])
    bloodline = StringField(u'血缘',validators=[Required()])
    traits = StringField(u'性状',validators=[Required()])
    submit = SubmitField(u'提交')
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS    

@app.route('/',methods=['POST','GET'])
def index(): 
    HABITAT = None
    BLOODLINE = None
    TRAITS = None
    IMGSITE = None
    form = SeachForm()
    if request.method == 'POST':
        #name = form.name.data
        #print name
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        values = cursor.execute('SELECT * FROM jianjie WHERE NAME=?',[request.form['name']])
        row = values.fetchall()
        
        if len(row) > 0:
            NAME = row[0][0]
            HABITAT = row[0][1]
            BLOODLINE = row[0][2]
            TRAITS = row[0][3]
            if row[0][4]:
                IMG = row[0][4]
                IMGSITE = os.path.join('static',IMG)
            return render_template('index.html',form=form,name=NAME,habitat=HABITAT,\
                           bloodline=BLOODLINE,traits=TRAITS,imgsite=IMGSITE)
        else:
            return render_template('index.html',data=None,form=form)
        cursor.close()
        conn.close()
#        form.name.data = ''   
    else:
        return render_template('index.html',form=form)

@app.route('/add',methods=['POST','GET'])
def add():
    print 'add work'
    form = AddForm()
    if request.method == 'POST':
        name = request.form['name']
        habitat = request.form['habitat']
        bloodline = request.form['bloodline']
        traits = request.form['traits']
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                print 'No selected file'
            else :
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    imgsite = filename
        print name,habitat,bloodline,traits,imgsite
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        values = cursor.execute('SELECT * FROM jianjie WHERE NAME=?',[name])
        row = values.fetchall()
        if len(row) > 0:
            print 'delete old data'
            cursor.execute('DELETE FROM jianjie WHERE NAME=?',[name])
        print 'write new data'
        cursor.execute('INSERT INTO jianjie (NAME,HABITAT,BLOODLINE,TRAITS,IMG) VALUES (?,?,?,?,?)',\
               [name,habitat,bloodline,traits,imgsite])
        conn.commit()
    return render_template('add.html',form=form)
    print 'add over'

    
if __name__ == '__main__':
    manager.run()
