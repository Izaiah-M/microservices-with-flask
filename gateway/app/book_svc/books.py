from flask import jsonify
import os, requests, traceback

book_service_url = f"http://{os.environ.get('BOOK_SVC_ADDRESS')}/create"


def create(req):
    author = req.get("author")
    bookname = req.get("bookname")
    genre = req.get("genre")

    if not author or not bookname or not genre:
        print("Bookname: " + bookname + "Genre: " + genre)
        print(author)
        return jsonify({"message": "Missing fields"}), 400

    book_data = {"author": author, "bookname": bookname, "genre": genre}

    response = requests.post("http://127.0.0.1:4000/api/book/create", json=book_data)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code

    # author = {"_id": ObjectId(author.id), "name": author.name, "email": author.email}
