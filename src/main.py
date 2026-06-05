from fastapi import FastAPI
from src.libs.vk.client import Client
from src.libs.infra.context import Context
from src.libs.infra.allocator import Allocator

allocator = Allocator()
context = Context(allocator)
app = FastAPI()


@app.get("/users")
def read_item():
    users = getUser()
    return {"users": users}

def getUser():
    db = context.pgDb
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return users
