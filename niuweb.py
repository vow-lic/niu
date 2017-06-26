#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:52:45 2017

@author: lic
"""
import os
import sys
import sqlite3
from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask_script import Manager

reload(sys)  
sys.setdefaultencoding('utf8') 

app = Flask(__name__)
app.config['WEBIMGSITE'] = os.path.join('http://127.0.0.1:5000','static')
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
    source = StringField(u'来源',validators=[Required()])
    submit = SubmitField(u'提交')
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS    

@app.route('/',methods=['POST','GET'])
def index(): 
    NAME = None
    HABITAT = None
    BLOODLINE = None
    TRAITS = None
    IMGSITE = None
    SOURCE = None
    form = SeachForm()
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    names = cursor.execute('SELECT NAME,ID FROM jianjie')
    NAMES = names.fetchall()
    if request.method == 'POST':
        #name = form.name.data
        #print name      
        values = cursor.execute('SELECT * FROM jianjie WHERE NAME=?',[request.form['name']])
        row = values.fetchall()       
        if len(row) > 0:
            NAME = row[0][0]
            HABITAT = row[0][1]
            BLOODLINE = row[0][2]
            TRAITS = row[0][3]
            if row[0][4]:
                IMG = row[0][4]
                IMGSITE = os.path.join(app.config['WEBIMGSITE'],IMG)
            SOURCE = row[0][5]
            return render_template('index.html',form=form,name=NAME,habitat=HABITAT,\
                           bloodline=BLOODLINE,traits=TRAITS,imgsite=IMGSITE,source=SOURCE,names=NAMES)
        else:
#            flash(u'您所查询的数据不存在')
            return render_template('index.html',data=None,form=form,names=NAMES)
    else:
        return render_template('index.html',form=form,names=NAMES)
    cursor.close()
    conn.close()

@app.route('/auto/<id>',methods=['POST','GET'])
def auto(id):
    NAME = None
    HABITAT = None
    BLOODLINE = None
    TRAITS = None
    IMGSITE = None
    SOURCE = None
    form = SeachForm()
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    names = cursor.execute('SELECT NAME,ID FROM jianjie')
    NAMES = names.fetchall()
    if request.method == 'POST':
        #name = form.name.data
        #print name      
        values = cursor.execute('SELECT * FROM jianjie WHERE NAME=?',[request.form['name']])
        row = values.fetchall()       
        if len(row) > 0:
            NAME = row[0][0]
            HABITAT = row[0][1]
            BLOODLINE = row[0][2]
            TRAITS = row[0][3]
            if row[0][4]:
                IMG = row[0][4]
                IMGSITE = os.path.join(app.config['WEBIMGSITE'],IMG)
            SOURCE = row[0][5]
            return render_template('index.html',form=form,name=NAME,habitat=HABITAT,\
                           bloodline=BLOODLINE,traits=TRAITS,imgsite=IMGSITE,source=SOURCE,names=NAMES)
        else:
#            flash(u'您所查询的数据不存在')
            return render_template('index.html',data=None,form=form,names=NAMES)
    else:
        values = cursor.execute('SELECT * FROM jianjie WHERE ID=?',[id])
        row = values.fetchall()       
        if len(row) > 0:
            NAME = row[0][0]
            HABITAT = row[0][1]
            BLOODLINE = row[0][2]
            TRAITS = row[0][3]
            if row[0][4]:
                IMG = row[0][4]
                IMGSITE = os.path.join(app.config['WEBIMGSITE'],IMG)
            SOURCE = row[0][5]
            return render_template('index.html',form=form,name=NAME,habitat=HABITAT,\
                           bloodline=BLOODLINE,traits=TRAITS,imgsite=IMGSITE,source=SOURCE,names=NAMES)
        else:
#            flash(u'您所查询的数据不存在')
            return render_template('index.html',data=None,form=form,names=NAMES)
    cursor.close()
    conn.close()

@app.route('/delete',methods=['POST','GET'])
def delete():
    HABITAT = None
    BLOODLINE = None
    TRAITS = None
    IMGSITE = None
    SOURCE = None
    form = SeachForm()
    print 'delete start'
    if request.method == 'POST':
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
                IMGSITE = os.path.join(app.config['WEBIMGSITE'],IMG)
            SOURCE = row[0][5]
            print 'delete begin'
            cursor.execute('DELETE FROM jianjie WHERE NAME=?',[NAME])
            conn.commit()
            if os.path.exists(os.path.join(app.root_path, 'static',IMG)):
                os.remove(os.path.join('static',IMG))
            print 'delete over'
            return render_template('delete.html',form=form,name=NAME,habitat=HABITAT,\
                           bloodline=BLOODLINE,traits=TRAITS,imgsite=IMGSITE,source=SOURCE)
        else:
            return render_template('delete.html',data=None,form=form)
        cursor.close()
        conn.close()
#        form.name.data = ''   
    else:
        return render_template('delete.html',form=form)
    
@app.route('/add',methods=['POST','GET'])
def add():
    print 'add start'
    form = AddForm()
    if request.method == 'POST':
        name = request.form['name']
        form.name.data = ''
        habitat = request.form['habitat']
        form.habitat.data = ''
        bloodline = request.form['bloodline']
        form.bloodline.data = ''
        traits = request.form['traits']
        form.traits.data = ''
        imgsite = None
        source = request.form['source']
        form.source.data = ''
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                print 'No selected file'
            else :
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    imgsite = filename
        print name,habitat,bloodline,traits,imgsite,source
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        values = cursor.execute('SELECT * FROM jianjie WHERE NAME=?',[name])
        row = values.fetchall()
        if len(row) > 0:
            print 'delete old data'
            cursor.execute('DELETE FROM jianjie WHERE NAME=?',[name])
        print 'write new data'
        cursor.execute('INSERT INTO jianjie (NAME,HABITAT,BLOODLINE,TRAITS,IMG,SOURCE) VALUES (?,?,?,?,?,?)',\
               [name,habitat,bloodline,traits,imgsite,source])
        conn.commit()
    return render_template('add.html',form=form)
    print 'add over'
   
if __name__ == '__main__':
    manager.run()
