from flask import jsonify
import os, requests

book_service_url = f"http://{os.environ.get('BOOK_SVC_ADDRESS')}/create"


def create(req):
    author = req.get("author")
    bookname = req.get("name")
    genre = req.get("genre")

    if not author or not bookname or not genre:
        return jsonify({"message": "Missing fields"}), 400

    book_data = {"author": author, "name": bookname, "genre": genre}

    response = requests.post("http://127.0.0.0:4000/api/book/create", json=book_data)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code

    # author = {"_id": ObjectId(author.id), "name": author.name, "email": author.email}
