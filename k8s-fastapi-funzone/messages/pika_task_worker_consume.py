# 2 Work queues
import asyncio
import json
import time
from asyncio import Task
from threading import current_thread
from typing import Optional

from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import StreamLostError
from pika.spec import Basic, BasicProperties
from uvicorn.config import logger

from messages.common import TASK_QUEUE_NAME
from messages.pika_common import establish_broker_connection, create_queue


channel = None  # type: Optional[BlockingChannel]
consumer_tag = None  # type: Optional[str]
start_consuming_task = None   # type: Optional[Task]


async def start_consuming():
    global channel, consumer_tag, start_consuming_task
    channel, connection = establish_broker_connection()
    create_queue(channel, TASK_QUEUE_NAME,
                 # Prevents loosing messages in case of RabbitMQ crash during processing,
                 # by saving it into storage.
                 # For stronger guarantee use "publisher confirms".
                 durable=True,
                 # Prevents new messages dispatch to a worker until it has
                 # processed and acknowledged the previous one,
                 # by dispatching it to the next worker that is not still busy.
                 fair_dispatch=True)

    consumer_tag = channel.basic_consume(TASK_QUEUE_NAME, callback, auto_ack=False)
    start_consuming_task = asyncio.create_task(asyncio.to_thread(channel.start_consuming))
    consuming_status = (f"[{TASK_QUEUE_NAME}][{consumer_tag}]\n Waiting for messages. "
                        f"To exit press CTRL+C")
    logger.info(consuming_status)

    return consuming_status


async def stop_consuming():
    global channel, consumer_tag, start_consuming_task
    if consumer_tag:
        try:
            channel.stop_consuming(consumer_tag)
        except StreamLostError:
            pass  # TODO: understand why this exception raises, and fix it
        consuming_status = f"[{TASK_QUEUE_NAME}] Stop waiting for messages. (consumer tag: {consumer_tag})"
        consumer_tag = None
    else:
        consuming_status = f"[{TASK_QUEUE_NAME}] Can't stop when not waiting for messages. (consumer tag: {consumer_tag})"

    logger.info(consuming_status)

    return consuming_status


def callback(channel_: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    consume_status = (f"[{TASK_QUEUE_NAME}][{method.consumer_tag}][{current_thread().name}]\n"
                      f" Received '{body.decode()}'")
    logger.info(consume_status)
    json_object = json.loads(body)
    time.sleep(json_object["sleep_seconds"])

    # Prevents loosing messages in case of worker termination during processing,
    # by re-queue that will redeliver it to another consumer.
    channel_.basic_ack(method.delivery_tag)
    consume_status = f"[{TASK_QUEUE_NAME}][{method.consumer_tag}]\n Acked"
    logger.info(consume_status)

    # To prevent memory consuming infinite messages redeliver due to unrelease of unacked messages:
    # sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
