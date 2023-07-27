from flask import Flask, request, jsonify
from auth_svc import access
from book_svc import books

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    # Get the login response from the access module
    print(request.json)
    try:
        res = access.login(request.json)
        return res
    except:
        return jsonify({"message": "Internal server error!"})


# for reaching book creation
@app.post("/create")
def createBook():
    try:
        res = books.create(request.json)
        return res
    except:
        return jsonify({"message": "Internal server error!"})


# if you want to use flask run command
# add a .flaskenv file and add your configurations..then do a flask run
# You'll get something like this
# Tip: There are .env or .flaskenv files present. Do "pip install python-dotenv" to use them.

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
