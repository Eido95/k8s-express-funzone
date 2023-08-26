import pika


USERNAME = 'k8s-funzone-apps'
PASSWORD = 'cvCB59XUYHL9x49'
HOST = "10.104.213.65"
PORT = "5672"  # default
VIRTUAL_HOST = "/"  # default
EXCHANGE = ''  # default
STRING_QUEUE_NAME = 'pika-string'


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
