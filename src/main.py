from fastapi import FastAPI
from src.libs.vk.client import Client
from src.libs.infra.context import Context 
context = Context()
app = FastAPI()


@app.get("/users")
def read_item(item_id: int, q: str | None = None):
    users = getUser()
    return {"users": users}

def getUser():
    db = context.pgDb

    db.execute("SELECT * FROM users")
    return db.fetchall()