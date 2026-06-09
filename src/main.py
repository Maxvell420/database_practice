import os
from fastapi import FastAPI
from src.libs.vk.client import Client
from src.libs.infra.context import Context
from src.libs.infra.allocator import Allocator
from src.libs.vk.vkLogger import VKLogger
allocator = Allocator()
context = Context(allocator)
app = FastAPI()

# Сейчас константа для файла логов, потом можно разделить на директорию и файл
LOG_PATH = str(os.getenv('LOG_DIR')) + '/' + str(os.getenv('LOG_FILE_PATH'))

@app.get("/users")
def read_item():
    logger = VKLogger(LOG_PATH)
    client = Client(context.secrets.vk.token, context.secrets.vk.group_id, logger)
    response = client.getUpdates()
    return response
