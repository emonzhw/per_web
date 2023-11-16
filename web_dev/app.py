import hashlib
from flask import Flask, request, redirect, render_template
import mysql.connector


app = Flask(__name__)
short_to_long = {}
domain = "http://127.0.0.1:5000/"

def connect_to_database():
    try:
        cnx = mysql.connector.connect(host="localhost",
                                      user="ez",
                                      password="password",
                                      database="demo")
    except mysql.connector.Error as err:
        print(err)
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            app.logger.error("Wrong username or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            app.logger.error("Database does not exist")
        else:
            app.logger.error(err)
    else:
        return cnx

@app.route('/register', methods=['GET', 'POST'])
def register():
    cnx = connect_to_database()   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        cur = cnx.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            return render_template('register.html', error='Username already taken') 
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        cnx.commit()
        cur.close() 
        return render_template('login.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    cnx = connect_to_database()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = cnx.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        
        if user:
            return redirect('admin') 
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    cnx = connect_to_database()
    print(short_to_long)
    return render_template('admin.html', records = short_to_long)

def generate_short_key(long_url):
    hash_object = hashlib.sha512(long_url.encode())
    return hash_object.hexdigest()[:10]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    custom_key = request.form['custom_key']
    if custom_key and custom_key in short_to_long:
        return render_template('index.html', error="Custom key already in use.", long_url=long_url, custom_key=custom_key)
    if not custom_key:
        custom_key = generate_short_key(long_url)
        while custom_key in short_to_long:
            custom_key = generate_short_key(long_url)
    short_url = domain + custom_key
    short_to_long[custom_key] = long_url
    return render_template('index.html', short_url=short_url)

@app.route('/<short_key>')
def redirect_to_long_url(short_key):
    long_url = short_to_long.get(short_key)
    if long_url:
        return redirect(long_url)
    else:
        return "URL nicht gefunden", 404

if __name__ == '__main__':
    app.run(debug=True)
