from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    sold = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    date_range = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)


class MyBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(
        db.Integer, db.ForeignKey("property.id", ondelete="CASCADE"), nullable=True
    )
    hotel = db.relationship(
        "Property", backref=db.backref("rents", cascade="all, delete")
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotel_id = db.Column(
        db.Integer, db.ForeignKey("property.id", ondelete="CASCADE"), nullable=False
    )
    hotel = db.relationship(
        "Property", backref=db.backref("transactions", cascade="all, delete")
    )
    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.now)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
