from flask import Flask, request, jsonify
from auth_svc import access
from book_svc import books
import traceback

app = Flask(__name__)


@app.put("/update-user/<string:id>")
def updateUserById(id):
    print(request.json)

    try:
        res = access.updateUser(id, request.json)
        return res
    except Exception as err:
        traceback.print_exc()
        return jsonify({"message": "Internal server error!"}), 500


@app.route("/login", methods=["POST"])
def login():
    # Get the login response from the access module
    print(request.json)

    try:
        res = access.login(request.json)
        return res
    except Exception as err:
        print(err)
        return jsonify({"message": "Internal server error!"}), 500


@app.route("/register", methods=["POST"])
def register():
    # Get the login response from the access module
    print(request.json)

    try:
        res = access.register(request.json)
        return res
    except Exception as err:
        print(err)
        return jsonify({"message": "Internal server error!"}), 500


# for reaching book creation
@app.post("/create-book")
def createBook():
    try:
        res = books.create(request.json)
        return res
    except Exception as err:
        traceback.print_exc()
        return jsonify({"message": "Internal server error!"}), 500


# if you want to use flask run command
# add a .flaskenv file and add your configurations..then do a flask run
# You'll get something like this
# Tip: There are .env or .flaskenv files present. Do "pip install python-dotenv" to use them.

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
