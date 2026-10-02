from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "candidate")

    if not name or not email or not password:
        return {
            "message": "Name, email and password are required"
        }, 400

    if role not in ["candidate", "recruiter"]:
        return {
            "message": "Invalid role"
        }, 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return {
            "message": "Email already registered"
        }, 409

    user = User(
        name=name,
        email=email,
        role=role
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User registered successfully",
        "user": user.to_dict()
    }, 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "message": "Email and password are required"
        }, 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user or not user.check_password(password):
        return {
            "message": "Invalid email or password"
        }, 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return {
        "message": "Login successful",
        "token": token,
        "user": user.to_dict()
    }, 200