import os, requests
from flask import jsonify, Blueprint


auth_service_url = f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login"

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


def login(req):
    username = req.get("username")
    password = req.get("password")

    # Check if username and password are present
    if not username or not password:
        return jsonify({"message": "Missing fields"}), 400

    # Create a dictionary with the credentials for authentication
    auth_data = {"username": username, "password": password}

    # Make the POST request to the auth service for login
    response = requests.post("http://127.0.0.1:5000/api/auth/login", json=auth_data)

    print(response.json())

    # Check the response from the auth service
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code


def register(req):
    username = req.get("username")
    password = req.get("password")
    email = req.get("email")

    # Check if username and password are present
    if not username or not password or not email:
        return jsonify({"message": "Missing fields"}), 400

    # Create a dictionary with the credentials for authentication
    auth_data = {"username": username, "password": password, "email": email}

    # Make the POST request to the auth service for login
    response = requests.post("http://127.0.0.1:5000/api/auth/register", json=auth_data)

    print(response.json())

    # Check the response from the auth service
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code


def updateUser(user_id, req):
    username = req.get("username")
    password = req.get("password")
    email = req.get("email")

    if not user_id or not username or not email:
        return jsonify({"message": "Missing fields"}), 400

    data = {"id": user_id, "username": username, "password": password, "email": email}

    response = requests.post("http://127.0.0.1:5000/api/auth/update", json=data)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code
