from dotenv import load_dotenv
import configparser
import os, sys
from flask import Flask
from utils import consumer
from service import books_service
from config import mongo

# from app.config import mongo
import threading

# Load environment variables from .env file
load_dotenv()

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.environ.get("DB_URI")
    mongo.init_app(app)

    app.register_blueprint(books_service.book_bp)

    app.config["DEBUG"] = True

    return app


if __name__ == "__main__":
    app = create_app()
    app.config["DEBUG"] = True

    # Start the RabbitMQ consumer in a separate thread

    # consumer_thread = threading.Thread(target=consumer.start_consumer)
    # consumer_thread.daemon = True
    # consumer_thread.start()

    try:
        consumer.start_consumer()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)

    port = 4000

    app.run(host="0.0.0.0", port=port, debug=True)
