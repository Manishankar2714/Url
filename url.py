from flask import Flask, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Function to generate a random string for the short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))  # You can adjust the length of the short URL
    return short_url

# Function to create the database table
def create_table():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY, long_url TEXT, short_url TEXT)''')
    conn.commit()
    conn.close()

# Function to store the long URL and its corresponding short URL in the database
def store_url(long_url, short_url):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, short_url))
    conn.commit()
    conn.close()

# Function to retrieve the long URL from the database based on the short URL
def get_long_url(short_url):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_url=?", (short_url,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

@app.route('/')
def index():
    return 'Welcome to URL Shortener!'

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_url = generate_short_url()
    store_url(long_url, short_url)
    return f'Shortened URL: {request.host_url}{short_url}'

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return 'URL not found'

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
