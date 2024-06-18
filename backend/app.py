from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

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

### Accommodations Routes ###

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accommodations")
    accommodations = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', accommodations=accommodations)

### Reviews Routes ###

@app.route('/reviews')
def reviews():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT reviews.*, users.username AS reviewer_name, accommodations.title AS accommodation_title
        FROM reviews
        JOIN users ON reviews.reviewer_id = users.id
        JOIN accommodations ON reviews.accommodation_id = accommodations.id
    """)
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('reviews.html', reviews=reviews)

@app.route('/review/new', methods=['GET', 'POST'])
def new_review():
    if request.method == 'POST':
        reviewer_id = request.form['reviewer_id']
        accommodation_id = request.form['accommodation_id']
        rating = request.form['rating']
        comment = request.form['comment']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reviews (reviewer_id, accommodation_id, rating, comment) 
            VALUES (%s, %s, %s, %s)
        """, (reviewer_id, accommodation_id, rating, comment))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('reviews'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT id, title FROM accommodations")
    accommodations = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('new_review.html', users=users, accommodations=accommodations)

@app.route('/review/<int:id>/edit', methods=['GET', 'POST'])
def edit_review(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        reviewer_id = request.form['reviewer_id']
        accommodation_id = request.form['accommodation_id']
        rating = request.form['rating']
        comment = request.form['comment']
        
        cursor.execute("""
            UPDATE reviews 
            SET reviewer_id = %s, accommodation_id = %s, rating = %s, comment = %s
            WHERE id = %s
        """, (reviewer_id, accommodation_id, rating, comment, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('reviews'))
    
    cursor.execute("SELECT * FROM reviews WHERE id = %s", (id,))
    review = cursor.fetchone()
    
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT id, title FROM accommodations")
    accommodations = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('edit_review.html', review=review, users=users, accommodations=accommodations)

@app.route('/review/<int:id>/delete', methods=['POST'])
def delete_review(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('reviews'))

### Bookings Routes ###

@app.route('/bookings')
def bookings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

@app.route('/booking/new', methods=['GET', 'POST'])
def new_booking():
    if request.method == 'POST':
        guest_id = request.form['guest_id']
        accommodation_id = request.form['accommodation_id']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        total_price = request.form['total_price']
        is_paid = request.form.get('is_paid') == 'on'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (guest_id, accommodation_id, check_in_date, check_out_date, total_price, is_paid) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (guest_id, accommodation_id, check_in_date, check_out_date, total_price, is_paid))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('bookings'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT id, title FROM accommodations")
    accommodations = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('new_booking.html', users=users, accommodations=accommodations)

@app.route('/booking/<int:id>/edit', methods=['GET', 'POST'])
def edit_booking(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        guest_id = request.form['guest_id']
        accommodation_id = request.form['accommodation_id']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        total_price = request.form['total_price']
        is_paid = request.form.get('is_paid') == 'on'
        
        cursor.execute("""
            UPDATE bookings 
            SET guest_id = %s, accommodation_id = %s, check_in_date = %s, check_out_date = %s, total_price = %s, is_paid = %s
            WHERE id = %s
        """, (guest_id, accommodation_id, check_in_date, check_out_date, total_price, is_paid, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('bookings'))
    
    cursor.execute("SELECT * FROM bookings WHERE id = %s", (id,))
    booking = cursor.fetchone()
    
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT id, title FROM accommodations")
    accommodations = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('edit_booking.html', booking=booking, users=users, accommodations=accommodations)

@app.route('/booking/<int:id>/delete', methods=['POST'])
def delete_booking(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('bookings'))

if __name__ == '__main__':
    app.run(debug=True)
