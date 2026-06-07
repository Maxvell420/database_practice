from fastapi import FastAPI
from src.libs.vk.client import Client
from src.libs.infra.context import Context
from src.libs.infra.allocator import Allocator

allocator = Allocator()
context = Context(allocator)
app = FastAPI()


@app.get("/users")
def read_item():
    client = Client(context.secrets.vk.token, context.secrets.vk.group_id)
    response = client.getUpdates()
    return response
