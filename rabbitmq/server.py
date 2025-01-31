import pika


def send_msg(msg : str):

# Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('193.203.160.234'))
    channel = connection.channel()

    # Declare a queue named 'hello'
    channel.queue_declare(queue='user1')

    # Publish a message to the 'hello' queue
    channel.basic_publish(exchange='',
                        routing_key='user1',
                        body= msg, properties= pika.BasicProperties(priority=1))

    print(f" [x] Sent {msg} to the client!")

    # Close the connection
    connection.close()
    

send_msg('Tejas Galande')