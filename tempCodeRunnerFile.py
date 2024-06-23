from flask import Flask, render_template, jsonify, request
from config import Config
from models import db, Booking, migrate
from auth import auth_blueprint
from hotel import hotel_blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

db.init_app(app)
migrate.init_app(app, db)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(hotel_blueprint, url_prefix="/api")


@app.route("/book", methods=["POST"])
@jwt_required()
def book():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    new_booking = Booking(
        user_id=current_user_id,
        image=data["image"],
        name=data["name"],
        details=data["details"],
        price=data["price"],
        rating=data["rating"],
    )
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/mybookings")
@jwt_required()
def my_bookings():
    current_user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=current_user_id).all()
    return render_template("Booking.html", bookings=bookings)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/stays")
def stays():
    return render_template("Stays.html")


if __name__ == "__main__":
    app.run(debug=True)
