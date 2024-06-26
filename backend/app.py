from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'airbnb'
app.config['MYSQL_HOST'] = 'localhost'

# Initialize MySQL
mysql = MySQL(app)

### Accommodations Routes ###
@app.route("/")
@app.route("/index")
def index():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accommodations")
        accommodations = cursor.fetchall()
        cursor.close()
        return render_template("index.html", accommodations=accommodations)
    except Exception as e:
        print("Error fetching accommodations:", e)
        return "An error occurred fetching accommodations."

### Reviews Routes ###

@app.route("/reviews")
def reviews():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            """
            SELECT reviews.*, users.username AS reviewer_name, accommodations.title AS accommodation_title
            FROM reviews
            JOIN users ON reviews.reviewer_id = users.id
            JOIN accommodations ON reviews.accommodation_id = accommodations.id
            """
        )
        reviews = cursor.fetchall()
        cursor.close()
        return render_template("reviews.html", reviews=reviews)
    except Exception as e:
        print("Error fetching reviews:", e)
        return "An error occurred fetching reviews."

@app.route("/review/new", methods=["GET", "POST"])
def new_review():
    try:
        if request.method == "POST":
            reviewer_id = request.form["reviewer_id"]
            accommodation_id = request.form["accommodation_id"]
            rating = request.form["rating"]
            comment = request.form["comment"]

            cursor = mysql.connection.cursor()
            cursor.execute(
                """
                INSERT INTO reviews (reviewer_id, accommodation_id, rating, comment) 
                VALUES (%s, %s, %s, %s)
                """,
                (reviewer_id, accommodation_id, rating, comment),
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("reviews"))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT id, title FROM accommodations")
        accommodations = cursor.fetchall()
        cursor.close()
        return render_template(
            "new_review.html", users=users, accommodations=accommodations
        )
    except Exception as e:
        print("Error in new_review():", e)
        return "An error occurred. Check logs for details."

    finally:
        if 'cursor' in locals():
            cursor.close()  # Always close cursor in finally block

@app.route("/review/<int:id>/edit", methods=["GET", "POST"])
def edit_review(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if request.method == "POST":
            reviewer_id = request.form["reviewer_id"]
            accommodation_id = request.form["accommodation_id"]
            rating = request.form["rating"]
            comment = request.form["comment"]

            cursor.execute(
                """
                UPDATE reviews 
                SET reviewer_id = %s, accommodation_id = %s, rating = %s, comment = %s
                WHERE id = %s
                """,
                (reviewer_id, accommodation_id, rating, comment, id),
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("reviews"))

        cursor.execute("SELECT * FROM reviews WHERE id = %s", (id,))
        review = cursor.fetchone()

        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT id, title FROM accommodations")
        accommodations = cursor.fetchall()
        cursor.close()
        return render_template(
            "edit_review.html", review=review, users=users, accommodations=accommodations
        )
    except Exception as e:
        print("Error in edit_review():", e)
        return "An error occurred. Check logs for details."

    finally:
        if 'cursor' in locals():
            cursor.close()  # Always close cursor in finally block

@app.route("/review/<int:id>/delete", methods=["POST"])
def delete_review(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM reviews WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("reviews"))
    except Exception as e:
        print("Error deleting review:", e)
        return "An error occurred deleting the review."

### Bookings Routes ###

@app.route("/bookings")
def bookings():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM bookings")
        bookings = cursor.fetchall()
        cursor.close()
        return render_template("bookings.html", bookings=bookings)
    except Exception as e:
        print("Error fetching bookings:", e)
        return "An error occurred fetching bookings."

@app.route("/booking/new", methods=["GET", "POST"])
def new_booking():
    try:
        if request.method == "POST":
            guest_id = request.form["guest_id"]
            accommodation_id = request.form["accommodation_id"]
            check_in_date = request.form["check_in_date"]
            check_out_date = request.form["check_out_date"]
            total_price = request.form["total_price"]
            is_paid = request.form.get("is_paid") == "on"

            cursor = mysql.connection.cursor()
            cursor.execute(
                """
                INSERT INTO bookings (guest_id, accommodation_id, check_in_date, check_out_date, total_price, is_paid) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    guest_id,
                    accommodation_id,
                    check_in_date,
                    check_out_date,
                    total_price,
                    is_paid,
                ),
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("bookings"))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT id, title FROM accommodations")
        accommodations = cursor.fetchall()
        cursor.close()
        return render_template(
            "new_booking.html", users=users, accommodations=accommodations
        )
    except Exception as e:
        print("Error in new_booking():", e)
        return "An error occurred. Check logs for details."

    finally:
        if 'cursor' in locals():
            cursor.close()  # Always close cursor in finally block

@app.route("/booking/<int:id>/edit", methods=["GET", "POST"])
def edit_booking(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if request.method == "POST":
            guest_id = request.form["guest_id"]
            accommodation_id = request.form["accommodation_id"]
            check_in_date = request.form["check_in_date"]
            check_out_date = request.form["check_out_date"]
            total_price = request.form["total_price"]
            is_paid = request.form.get("is_paid") == "on"

            cursor.execute(
                """
                UPDATE bookings 
                SET guest_id = %s, accommodation_id = %s, check_in_date = %s, check_out_date = %s, total_price = %s, is_paid = %s
                WHERE id = %s
                """,
                (
                    guest_id,
                    accommodation_id,
                    check_in_date,
                    check_out_date,
                    total_price,
                    is_paid,
                    id,
                ),
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("bookings"))

        cursor.execute("SELECT * FROM bookings WHERE id = %s", (id,))
        booking = cursor.fetchone()

        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT id, title FROM accommodations")
        accommodations = cursor.fetchall()
        cursor.close()
        return render_template(
            "edit_booking.html", booking=booking, users=users, accommodations=accommodations
        )
    except Exception as e:
        print("Error in edit_booking():", e)
        return "An error occurred. Check logs for details."

    finally:
        if 'cursor' in locals():
            cursor.close()  # Always close cursor in finally block

@app.route("/booking/<int:id>/delete", methods=["POST"])
def delete_booking(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("bookings"))
    except Exception as e:
        print("Error deleting booking:", e)
        return "An error occurred deleting the booking."


@app.route("/schema")
def schema():
    return render_template("schema.html")

# @app.route("/reviews1")
# def schema1():
#     return render_template("reviews.html")

# @app.route("/booking1")
# def schema2():
#     return render_template("bookings.html")

# @app.route("/acc1")
# def schema3():
#     return render_template("nc.html")

@app.route("/accommodations")
def accommodations():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accommodations")
        accommodations = cursor.fetchall()
        cursor.close()
        return render_template("allacc.html", accommodations1=accommodations)
    except Exception as e:
        print("Error fetching accommodations:", e)
        return "An error occurred fetching accommodations."

@app.route("/accommodation/new", methods=["GET", "POST"])
def new_accommodation():
    try:
        if request.method == "POST":
            title = request.form["title"]
            description = request.form.get("description", "")
            city = request.form["city"]
            country = request.form["country"]
            address = request.form.get("address", "")
            price_per_night = request.form["price_per_night"]
            num_bedrooms = request.form["num_bedrooms"]
            num_bathrooms = request.form["num_bathrooms"]
            max_guests = request.form["max_guests"]
            host_id = request.form.get("host_id", None)

            cursor = mysql.connection.cursor()
            cursor.execute(
                """
                INSERT INTO accommodations 
                (title, description, city, country, address, price_per_night, num_bedrooms, num_bathrooms, max_guests, host_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    title, description, city, country, address, price_per_night,
                    num_bedrooms, num_bathrooms, max_guests, host_id
                ),
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("accommodations"))

        # Fetch hosts for dropdown
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, username FROM users WHERE is_host = TRUE")
        hosts = cursor.fetchall()
        cursor.close()

        return render_template("new_accommodation.html", hosts=hosts)
    except Exception as e:
        print("Error in new_accommodation():", e)
        return "An error occurred adding new accommodation."

# @app.route("/accommodation/<int:id>/edit", methods=["GET", "POST"])
# def edit_accommodation(id):
#     try:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#         if request.method == "POST":
#             title = request.form["title"]
#             description = request.form.get("description", "")
#             city = request.form["city"]
#             country = request.form["country"]
#             address = request.form.get("address", "")
#             price_per_night = request.form["price_per_night"]
#             num_bedrooms = request.form["num_bedrooms"]
#             num_bathrooms = request.form["num_bathrooms"]
#             max_guests = request.form["max_guests"]
#             host_id = request.form.get("host_id", None)

#             cursor.execute(
#                 """
#                 UPDATE accommodations 
#                 SET title = %s, description = %s, city = %s, country = %s, address = %s, 
#                     price_per_night = %s, num_bedrooms = %s, num_bathrooms = %s, max_guests = %s, host_id = %s 
#                 WHERE id = %s
#                 """,
#                 (
#                     title, description, city, country, address, price_per_night,
#                     num_bedrooms, num_bathrooms, max_guests, host_id, id
#                 ),
#             )
#             mysql.connection.commit()
#             cursor.close()
#             return redirect(url_for("accommodations"))

#         cursor.execute("SELECT * FROM accommodations WHERE id = %s", (id,))
#         accommodation = cursor.fetchone()

#         # Fetch hosts for dropdown
#         cursor.execute("SELECT id, username FROM users WHERE is_host = TRUE")
#         hosts = cursor.fetchall()
#         cursor.close()

#         return render_template("edit_accommodation.html", accommodation=accommodation, hosts=hosts)
#     except Exception as e:
#         print("Error in edit_accommodation():", e)
#         return "An error occurred editing accommodation."

# @app.route("/accommodation/<int:id>/delete", methods=["POST"])
# def delete_accommodation(id):
#     try:
#         cursor = mysql.connection.cursor()
#         cursor.execute("DELETE FROM accommodations WHERE id = %s", (id,))
#         mysql.connection.commit()
#         cursor.close()
#         return redirect(url_for("accommodations"))
#     except Exception as e:
#         print("Error deleting accommodation:", e)
#         return "An error occurred deleting the accommodation."



    



# Route to update accommodation




if __name__ == "__main__":
    app.run(debug=True)
