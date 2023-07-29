import json
import subprocess

from fastapi import FastAPI
from starlette.responses import Response
from uvicorn.config import logger

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


def get_response_body():
    return {
        "app": "fastapi",
        "hostname": run("hostname"),
        "ips": run("hostname -I")
    }


def run(command: str):
    return subprocess.run(command.split(), stdout=subprocess.PIPE, check=True).stdout.decode().strip()
