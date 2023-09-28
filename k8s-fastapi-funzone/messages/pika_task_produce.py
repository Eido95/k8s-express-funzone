# 2 Work queues
import json
import random

from pika import BasicProperties
from pika.spec import PERSISTENT_DELIVERY_MODE
from uvicorn.config import logger

from messages.common import TASK_QUEUE_NAME, EXCHANGE
from messages.pika_common import establish_broker_connection, create_queue, flush_network_buffers


def produce_task(content):
    channel, connection = establish_broker_connection()
    create_queue(channel, TASK_QUEUE_NAME,
                 # Prevents loosing a message in case of RabbitMQ crash during
                 # processing, by saving it into storage.
                 # For stronger guarantee use "publisher confirms".
                 durable=True)

    # Marks a message as persistent.
    properties = BasicProperties(delivery_mode=PERSISTENT_DELIVERY_MODE)
    body = json.dumps({
        "content": content,
        "sleep_seconds": random.randint(10, 20)
    })
    channel.basic_publish(EXCHANGE, TASK_QUEUE_NAME, body, properties)
    publish_status = f"[{TASK_QUEUE_NAME}] Sent '{body}'"
    logger.info(publish_status)

    flush_network_buffers(connection)

    return publish_status
