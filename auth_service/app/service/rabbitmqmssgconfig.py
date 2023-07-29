import pika, json


# To handle user_update_message
def publish_user_update(message):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare a queue to publish the user update message
    channel.queue_declare(queue="user_updates", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="user_updates",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )

    # Close the connection
    connection.close()
