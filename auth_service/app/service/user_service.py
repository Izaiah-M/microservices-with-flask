from flask import Blueprint, request, jsonify
from ..config import mongo

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.get("/")
@auth_bp.get("/index")
def hello():
    users_collection = mongo.db.users

    users = users_collection.find()

    users_list = [
        {"_id": str(user["_id"]), "username": user["username"]} for user in users
    ]

    return jsonify({"users": users_list}), 200


@auth_bp.post("/register")
def register_user():
    # Picking our users instance in the db
    users_collection = mongo.db.users
    username = request.json.get("username")
    password = request.json.get("password")

    # print(username)
    # print(password)

    if not username:
        return jsonify({"message": "Username is required!"}), 400

    if not password:
        return jsonify({"message": "Password is required!"}), 400

    user_doc = {"username": username, "password": password}

    users_collection.insert_one(user_doc)

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.post("/login")
def login_user():
    users_collection = mongo.db.users
    username = request.json.get("username")
    password = request.json.get("password")

    if not username:
        return jsonify({"message": "Username is required!"}), 400

    if not password:
        return jsonify({"message": "Password is required!"}), 400

    # Find the user by username in the database
    user = users_collection.find_one({"username": username})

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Check if the provided password matches the stored password
    if user["password"] == password:
        # Passwords match, login successful
        return jsonify({"message": "Login successful"}), 200
    else:
        # Passwords do not match, login failed
        return jsonify({"message": "Invalid credentials"}), 401
