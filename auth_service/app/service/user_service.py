from flask import Blueprint, request, jsonify
from config import mongo
from bson.objectid import ObjectId  # Import ObjectId to handle MongoDB's _id field
from . import rabbitmqmssgconfig

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
    email = request.json.get("email")

    # print(username)
    # print(password)

    if not username or not email:
        return jsonify({"message": "Username and email required!"}), 400

    if not password:
        return jsonify({"message": "Password is required!"}), 400

    user_doc = {"name": username, "password": password, "email": email}

    users_collection.insert_one(user_doc)

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.post("/update")
def updateUser():
    users_collection = mongo.db.users
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    user_id = request.json.get("id")

    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    user = users_collection.find_one({"_id": ObjectId(user_id)})

    # Check if the user was found
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Save a copy of the original user document for rollback incase of messages failing to be added to the queue
    original_user = user.copy()

    # Create the update dictionary with the fields to update
    update_fields = {}
    if username:
        update_fields["name"] = username
    if password:
        update_fields["password"] = password
    if email:
        update_fields["email"] = email

    result = users_collection.update_one({"_id": user["_id"]}, {"$set": update_fields})

    # Check if the update was successful
    if result.modified_count == 1:
        # Publish a user update message to RabbitMQ
        message = {
            "user_id": str(user["_id"]),  # Convert ObjectId to string for serialization
            "updated_fields": update_fields,
        }
        try:
            rabbitmqmssgconfig.publish_user_update(message)
        except Exception as err:
            # Rollback the user update
            print("Something happened with rabbitmq: ", err)
            users_collection.update_one({"_id": user["_id"]}, {"$set": original_user})
            return jsonify({"message": "Internal server error, please try again"}), 500

        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "Failed to update user. Please try again"}), 500


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
