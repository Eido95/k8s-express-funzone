from uvicorn.config import logger

from messages.pika_common import establish_broker_connection, create_queue, EXCHANGE, flush_network_buffers, \
    STRING_QUEUE_NAME


def produce_string(body):
    channel, connection = establish_broker_connection()
    create_queue(channel, STRING_QUEUE_NAME)

    channel.basic_publish(EXCHANGE, STRING_QUEUE_NAME, body=body)
    publish_status = f"[{STRING_QUEUE_NAME}] Sent '{body}'"
    logger.info(publish_status)

    flush_network_buffers(connection)

    return publish_status
