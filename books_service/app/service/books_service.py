from flask import Blueprint, request, jsonify
from ..config import mongo
from bson.objectid import ObjectId

book_bp = Blueprint("book", __name__, url_prefix="/api/book")


@book_bp.post("/create")
def create_book():
    books = mongo.db.books

    authorId = request.json.get("authorId")
    name = request.json.get("name")
    genre = request.json.get("genre")

    if not authorId:
        return jsonify({"message": "Please provide all required fields"}), 400

    if not name:
        return jsonify({"message": "Please provide all required fields"}), 400

    if not genre:
        return jsonify({"message": "Please provide all required fields"}), 400

    book_doc = {"authorId": ObjectId(authorId), "name": name, "genre": genre}

    books.insert_one(book_doc)

    return jsonify({"message": "book created"}), 201
