from fastapi import FastAPI
from src.libs.vk.client import Client
app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    client = Client()
    json = client.get()
    return {"json": json}
