from flask import Flask
from flask import render_template, request, session, url_for, redirect, flash, g
import sqlite3
import config

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('FLASK_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.db = sqlite3.connect(app.config['DATABASE'])

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if 'user' in session:
        return render_template('hello.html', name=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['user']
        passwd = request.form['passwd']
        cursor = g.db.execute('select * from users where name=? and password=?', [name, passwd])
        if cursor.fetchone() is not None:
            session['user'] = name
            flash('Login successfully!')
            return redirect(url_for('index'))
        else:
            flash('No such user!', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'), 302)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
from functools import wraps
def authorize(fn):
    @wraps(fn)
    def wrapper(*args, **kwds):
        user = session.get('logged_in', None)
        if user:
            return fn(user=user)
        else:
            return redirect(url_for('signin',next=request.path))

    return wrapper
    

@app.route('/home')
@authorize
def home(**kwds):
    username = kwds['user']
    return render_template('index.html' ,username=username)
    
#加密存储密码
import os
import hashlib
def encrypt_password(password, salt=None, encryptlop=30):
    if not salt:
        salt = os.urandom(16).encode('hex') # length 32
    for i in range(encryptlop):
        password = hashlib.sha256(password + salt).hexdigest() # length 64
    return password, salt
    
#简单的错误处理
class loginError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# 注册登录（下面的代码没有实际运行过）
# 连接数据库我是使用的是 mysql.connector 
# http://dev.mysql.com/downloads/connector/python/
# 写法和常用的MySQL-python稍有所不同
# 下面没有连接数据库的代码

@app.route('/register/', methods=['GET','POST'])
def request():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        # 这里最好需要验证用户输入，我就不写了
        u = request.form['username']
        p,s = encrypt_password(request.form['password'])
        g.db.cursor.execute('INSERT INTO users (name,password,salt) VALUES (%s,%s,%s)',(u,p,s,)
        g.db.commit()
        return redirect(url_for('signin'))
        
@app.route('/signin/', methods=['GET','POST'])
def signin():
    if request.method == 'GET':
        referrer = request.args.get('next','/')
        return render_template("login.html",next=referrer)
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        n = request.form['next']
        try:
            g.db.cursor.execute('SELECT `name` FROM users WHERE name = %s',(u,))
            if not g.db.cursor.fetchone():
                raise loginError(u'错误的用户名或者密码!')
            g.db.cursor.execute('SELECT `salt`,`password` FROM users WHERE name = %s',(u,))
            salt,password = g.db.cursor.fetchone()
            if encrypt_password(p,salt)[0] == password:
                session['logged_in'] = u
                return redirect(next)
            else:
                raise loginError(u'错误的用户名或者密码!')
        except loginError as e:
            return render_template('login.html', next=next,error=e.value)

@app.route('/signout/', methods=['POST'])
def signout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))
