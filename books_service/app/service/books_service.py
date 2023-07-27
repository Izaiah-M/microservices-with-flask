from flask import Blueprint, request, jsonify
from ..config import mongo
from bson.objectid import ObjectId

book_bp = Blueprint("book", __name__, url_prefix="/api/book")


@book_bp.post("/create")
def create_book():
    books = mongo.db.books

    author = request.json.get("author")
    bookname = request.json.get("name")
    genre = request.json.get("genre")

    author = {"_id": ObjectId(author.id), "name": author.name, "email": author.email}

    if not author or not bookname or not genre:
        return jsonify({"message": "Missing fields"}), 400

    book_doc = {"author": author, "name": bookname, "genre": genre}

    books.insert_one(book_doc)

    return jsonify({"message": "book created"}), 201
