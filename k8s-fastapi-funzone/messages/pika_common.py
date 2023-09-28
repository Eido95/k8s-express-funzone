import pika
from pika.adapters.blocking_connection import BlockingChannel

from messages.common import USERNAME, PASSWORD, HOST, PORT, VIRTUAL_HOST


def create_queue(channel: BlockingChannel, queue_name, durable=False, fair_dispatch=False):
    channel.queue_declare(queue_name, durable=durable)

    if fair_dispatch:
        # Don't give more than one message to a worker at a time.
        channel.basic_qos(prefetch_count=1)


def establish_broker_connection():
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    parameters = pika.ConnectionParameters(HOST, PORT, VIRTUAL_HOST, credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    return channel, connection


def flush_network_buffers(connection):
    connection.close()
