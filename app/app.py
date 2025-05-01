from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os
import redis
import socket
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Redis session store
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database='auth_db',
        user='user',
        password='password'
    )
    return conn

@app.before_request
def log_request_info():
    print("\n🔹 [Request] Method:", request.method)
    print("🔹 [Request] Path:", request.path)
    print("🔹 [Request] Cookies:", request.cookies)
    print("🔹 [Request] Session:", dict(session))

@app.route('/')
def index():
    if 'username' in session:
        hostname = socket.gethostname()
        print(f"📘 [Dashboard] User {session['username']} served by {hostname}")
        return render_template('dashboard.html', username=session['username'], hostname=hostname)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        print(f"📝 [Register] New user: {username}")

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cur.close()
            conn.close()
            print(f"✅ [Register] User {username} registered successfully")
            return redirect(url_for('login'))
        except Exception as e:
            print(f"❌ [Register Error] {e}")
            return 'Registration failed', 500

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"🔐 [Login Attempt] Username: {username}")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['username'] = username
            print(f"✅ [Login Success] Session created for user: {username}")
            r.set(username, 'loggedin')
            print(f"🧠 [Redis] Set session key for {username}")
            return redirect(url_for('index'))

        print("❌ [Login Failed] Invalid credentials")
        return 'Invalid credentials', 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    username = session.pop('username', None)
    if username:
        r.delete(username)
        print(f"🚪 [Logout] Session cleared and Redis key deleted for {username}")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)