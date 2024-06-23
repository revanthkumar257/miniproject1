from flask import Blueprint, request, jsonify, render_template
from models import db, Booking, Property
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.to_dict import to_dict

hotel_blueprint = Blueprint("hotel", __name__)


@hotel_blueprint.route("/book", methods=["POST"])
@jwt_required()
def book_hotel():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    try:
        new_booking = Property(
            user_id=current_user_id,
            title=data["name"],
            description=data["description"],
            price=data["price"],
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error ": "hotel not"})


@hotel_blueprint.route("/get_hotel")
@jwt_required()
def booking():
    hotels = Property.query.all()
    hotel_data = []

    for hotel in hotels:
        if not hotel.sold:
            hotel_data.append(to_dict(hotel))

    return jsonify(hotel_data), 200


@hotel_blueprint.route("/buy/<int:hotel_id>", methods=["POST"])
@jwt_required()
def buy_vehicle(hotel_id):
    current_user = get_jwt_identity()

    hotel = Property.query.get(hotel_id)

    if not hotel:
        return jsonify({"message": "Hotel not found"}), 404

    if hotel.user_id == current_user:
        return jsonify({"message": "You cannot buy your own Hotel"}), 400

    # transaction = Transaction(vehicle_id=vehicle.id, buyer_id=current_user, seller_id=vehicle.user_id, amount=vehicle.price)
    # db.session.add(transaction)
    hotel.sold = True
    db.session.commit()

    return jsonify({"message": "Hotel booked successfully!"}), 200
