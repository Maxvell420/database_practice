import os
from fastapi import FastAPI
from src.libs.vk.client import Client
from src.libs.infra.context import Context
from src.libs.infra.allocator import Allocator
from src.libs.vk.vkLogger import VKLogger
from src.libs.nasapower.client import Client as NasapowerClient
from src.domain.map.repositories.nasaPowerRepository import NasaPowerRepository
from src.domain.map.useCases.nasaPower import NasaPower
allocator = Allocator()
context = Context(allocator)
app = FastAPI()
from src.libs.nspd.client import Client as NspdClient
# Сейчас константа для файла логов, потом можно разделить на директорию и файл
LOG_PATH = str(os.getenv('LOG_DIR')) + '/' + str(os.getenv('LOG_FILE_PATH'))

@app.get("/users")
async def read_item():
    repository = NasaPowerRepository(await context.pgDb())
    data = await repository.getByGeohashAndDate('xxx', 12)
    # nasapowerClient = NasapowerClient(logger)
    # response = nasapowerClient.getDataByPointHourly(20260101, 20260616, 59.887, 30.3095)
    return data
