from flask import Flask
import pika

app = Flask(__name__)

# Configruing rabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()
