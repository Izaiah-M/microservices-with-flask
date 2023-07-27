import os, requests
from flask import jsonify


auth_service_url = f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login"


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
