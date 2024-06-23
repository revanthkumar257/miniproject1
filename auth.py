from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from models import db, bcrypt, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_blueprint = Blueprint('auth', __name__)

def to_dict(self):
    return {
        'id': self.id,
        'username': self.username,
        'email': self.email,
        'created_at': self.created_at.isoformat(),
        'updated_at': self.updated_at.isoformat()
    }

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    fName = data["fName"]
    lName = data["lName"]
    email = data["email"]
    password = data["password"]

    username = fName + " " + lName

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already exists. Please sign in.'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"data": to_dict(user), "token": access_token})

@auth_blueprint.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user.to_dict())