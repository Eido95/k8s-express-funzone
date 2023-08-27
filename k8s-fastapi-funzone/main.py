import json
import subprocess

from fastapi import FastAPI
from starlette.responses import Response
from uvicorn.config import logger

from messages.pika_consume import start_string_consuming
from messages.pika_produce import produce_string

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
    return get_response_body()


@app.get("/pika/produce/string")
async def pika_produce_string():
    response_body = get_response_body()
    body = (f'app {response_body["app"]}, hostname {response_body["hostname"]}, '
            f'ips {response_body["ips"]}')
    return produce_string(body)


@app.get("/pika/consume/string")
async def pika_consume_string():
    return await start_string_consuming()


def get_response_body():
    return {
        "app": "fastapi",
        "hostname": run("hostname"),
        "ips": run("hostname -I")
    }


def run(command: str):
    return subprocess.run(command.split(), stdout=subprocess.PIPE, check=True).stdout.decode().strip()
