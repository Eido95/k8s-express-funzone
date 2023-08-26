from threading import Thread

from pika.channel import Channel
from pika.spec import Basic, BasicProperties
from uvicorn.config import logger

from messages.pika_common import establish_broker_connection, STRING_QUEUE_NAME, create_queue


def start_string_consuming():
    channel, connection = establish_broker_connection()
    create_queue(channel, STRING_QUEUE_NAME)

    channel.basic_consume(STRING_QUEUE_NAME, callback, auto_ack=True)
    Thread(target=channel.start_consuming).start()
    consuming_status = f"[{STRING_QUEUE_NAME}] Waiting for messages. To exit press CTRL+C"
    logger.info(consuming_status)

    return consuming_status


def callback(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    publish_status = f"[{STRING_QUEUE_NAME}] Received '{body.decode()}'"
    logger.info(publish_status)
