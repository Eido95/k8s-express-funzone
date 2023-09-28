import json
import subprocess

from fastapi import FastAPI
from starlette.responses import Response
from uvicorn.config import logger

from log.ecs_log import logger as ecs_logger
from messages import (pika_queue_consume, pika_queue_produce, pika_task_produce,
                      pika_task_worker_consume)

app = FastAPI()

logger.info(f"k8s FastAPI Fun Zone app")


@app.exception_handler(404)
async def handle_not_found(request, exception):
    return Response(
        content=f"Sorry can't find that! {json.dumps(get_response_body())}",
        status_code=404
    )


@app.get("/")
async def root():
    ecs_logger.debug("Responding to / request", extra={"http.request.method": "get"})
    return get_response_body()


@app.post("/pika/queue/produce/string")
async def pika_queue_produce_string():
    response_body = get_response_body()
    body = (f'library "pika", app {response_body["app"]}, hostname {response_body["hostname"]}, '
            f'ips {response_body["ips"]}')
    return pika_queue_produce.produce_string(body)


@app.post("/pika/queue/consume/string")
async def pika_queue_consume_string():
    return await pika_queue_consume.start_string_consuming()


@app.delete("/pika/queue/consume/string")
async def pika_queue_stop_consume_string():
    return await pika_queue_consume.stop_string_consuming()


@app.post("/pika/task/produce")
async def pika_produce_task():
    response_body = get_response_body()
    body = (f'library "pika", app {response_body["app"]}, hostname {response_body["hostname"]}, '
            f'ips {response_body["ips"]}')
    return pika_task_produce.produce_task(body)


@app.post("/pika/task/consume")
async def pika_consume_task():
    return await pika_task_worker_consume.start_consuming()


@app.delete("/pika/task/consume")
async def pika_stop_task_consume():
    return await pika_task_worker_consume.stop_consuming()


def get_response_body():
    return {
        "app": "fastapi",
        "hostname": run("hostname"),
        "ips": run("hostname -I")
    }


def run(command: str):
    return subprocess.run(command.split(), stdout=subprocess.PIPE, check=True).stdout.decode().strip()
