import pika, json
from config import mongo
from bson.objectid import ObjectId


# RabbitMQ consumer function to handle user update messages
def process_user_update_callback(ch, method, properties, body):
    books_collection = mongo.db.books

    # Getting the updated fields from our message body
    try:
        message = json.loads(body)
        user_id = message.get("user_id")
        updated_fields = message.get("updated_fields")

        print("Started updating necessary fields....")
        # Check if the "name" field was updated
        if "name" in updated_fields:
            # Perform the update in the books collection
            result = books_collection.update_many(
                {"author._id": ObjectId(user_id)},
                {"$set": {"author.name": updated_fields["name"]}},
            )

            print(f"Updated {result.modified_count} book(s) with the new author name.")

        if "email" in updated_fields:
            # Perform the update in the books collection
            books_collection = mongo.db.books
            result = books_collection.update_many(
                {"author._id": ObjectId(user_id)},
                {"$set": {"author.email": updated_fields["email"]}},
            )

        # Acknowledge the message to remove it from the queue
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as err:
        print(err)
        # Don't acknolwedge the message and leave it in the queue
        ch.basic_nack(delivery_tag=method.delivery_tag)


# Function to start the RabbitMQ consumer
def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Declare the user_updates queue
    channel.queue_declare(queue="user_updates", durable=True)

    # Set up the consumer to process messages from the queue
    channel.basic_consume(
        queue="user_updates", on_message_callback=process_user_update_callback
    )

    print(
        "RabbitMQ consumer started in the Book service. Waiting for user update messages..."
    )
    channel.start_consuming()
