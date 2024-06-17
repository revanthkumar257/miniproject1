from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'localhost',
    'password': '12345678',
    'host': 'localhost',
    'database': 'airbnb'
}

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schema')
def schema():
    return render_template('schema.html')

@app.route('/reviews')
def reviews():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('reviews.html', reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
