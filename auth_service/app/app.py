import configparser
import os
from flask import Flask
from service import user_service

from config import mongo

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.environ.get("DB_URI")
    mongo.init_app(app)

    app.register_blueprint(user_service.auth_bp)

    app.config["DEBUG"] = True

    return app


if __name__ == "__main__":
    app = create_app()
    app.config["DEBUG"] = True

    port = 5000

    app.run(debug=True, host="0.0.0.0", port=port)
