#!/usr/bin/python
#-*- coding: UTF-8 -*-
import sqlite3
import time
from flask import (Flask, render_template, g, session, redirect, url_for, request)

SECRET_KEY = 'This is my key'
DATABASE = './flaskr.db'
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'admin'
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
	g.db.close()


@app.route('/')
def show_video():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html',user=session['user'])


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users')
        for user in cur.fetchall():
            print(user)
            if user[0]==request.form['username'] and str(user[1])==str(request.form['password']): 
                session['logged_in'] = True
                session['user']=request.form['username']
                return redirect(url_for('show_video'))
    return render_template('login.html')

@app.route('/register/',methods=['POST'])
def register():
	if request.form['password'] == request.form['password2']:
		g.db.execute('insert into users (username, password) values (?, ?)',[request.form['username'], request.form['password']])
		g.db.commit()   
		session['user']=request.form['username']
		return render_template('success.html',user=session['user'])
	return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/share/')
def share():
	cur = g.db.execute('select title, text,now,name from entries order by id desc')
	entries = [dict(title=row[0],text=row[1],now=row[2],name=row[3]) for row in cur.fetchall()]
	return render_template('share.html',entries=entries,user=session['user'])		

@app.route('/add/',methods=[ 'POST'])
def add_entries():
	if not session.get('logged_in'):
		abort(401)
	now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	g.db.execute('insert into entries (title,text,now,name) values (?, ?,?,?)',[request.form['title'], request.form['text'],now,str(session['user'])])
	g.db.commit()   
	return redirect(url_for('share'))

