import pika

from messages.common import USERNAME, PASSWORD, HOST, PORT, VIRTUAL_HOST


def create_queue(channel, queue_name):
    channel.queue_declare(queue_name)


def establish_broker_connection():
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    parameters = pika.ConnectionParameters(HOST, PORT, VIRTUAL_HOST, credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    return channel, connection


def flush_network_buffers(connection):
    connection.close()
