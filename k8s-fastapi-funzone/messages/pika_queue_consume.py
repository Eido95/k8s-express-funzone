# 1 "Hello World!"
import asyncio
from asyncio import Task
from typing import Optional

from pika.adapters.blocking_connection import BlockingChannel
from pika.channel import Channel
from pika.exceptions import StreamLostError
from pika.spec import Basic, BasicProperties
from uvicorn.config import logger

from messages.common import STRING_QUEUE_NAME
from messages.pika_common import establish_broker_connection, create_queue


channel = None  # type: Optional[BlockingChannel]
consumer_tag = None  # type: Optional[str]
start_consuming_task = None   # type: Optional[Task]


async def start_string_consuming():
    global channel, consumer_tag, start_consuming_task
    channel, connection = establish_broker_connection()
    create_queue(channel, STRING_QUEUE_NAME)

    consumer_tag = channel.basic_consume(STRING_QUEUE_NAME, callback, auto_ack=True)
    start_consuming_task = asyncio.create_task(asyncio.to_thread(channel.start_consuming))
    consuming_status = (f"[{STRING_QUEUE_NAME}] Waiting for messages. "
                        f"To exit press CTRL+C (consumer tag: {consumer_tag})")
    logger.info(consuming_status)

    return consuming_status


async def stop_string_consuming():
    global channel, consumer_tag, start_consuming_task
    if consumer_tag:
        try:
            channel.stop_consuming(consumer_tag)
        except StreamLostError:
            pass  # TODO: understand why this exception raises, and fix it
        consuming_status = f"[{STRING_QUEUE_NAME}] Stop waiting for messages. (consumer tag: {consumer_tag})"
        consumer_tag = None
    else:
        consuming_status = f"[{STRING_QUEUE_NAME}] Can't stop when not waiting for messages. (consumer tag: {consumer_tag})"

    logger.info(consuming_status)

    return consuming_status


def callback(channel_: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    publish_status = f"[{STRING_QUEUE_NAME}] Received '{body.decode()}'"
    logger.info(publish_status)
