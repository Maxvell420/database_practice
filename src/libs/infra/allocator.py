from os import getenv
from dotenv import load_dotenv
from psycopg2 import connect as psycopg2Connect

from .parts.pg import PGParts
from .secrets import Secrets
from .parts.vk import VKParts


load_dotenv()
class Allocator:
    def __init__(self):
        self._secrets: Secrets | None = None
        self._pg_db: psycopg2Connect | None = None

    @property
    def secrets(self) -> Secrets:
        if self._secrets is None:
            self._secrets = self.loadSecrets()
        return self._secrets

    @property
    def pgDb(self) -> psycopg2Connect:
        if self._pg_db is None:
            self._pg_db = self.loadPgDb()
        return self._pg_db

    def loadSecrets(self) -> Secrets:
        return Secrets(pg=self.loadPgParts(), vk=self.loadVkParts())

    def loadPgParts(self) -> PGParts:
        # подумать в будущем как лучше сделать это
        return PGParts(
            host=getenv('DB1_HOST'),
            port=getenv('DB1_PORT'),
            user=getenv('DB1_USER'),
            password=getenv('DB1_PASSWORD'),
            database=getenv('DB1_DATABASE')
        )

    def loadVkParts(self) -> VKParts:
        return VKParts(
            token=getenv('VK_TOKEN')
        )

    def loadPgDb(self) -> psycopg2Connect:
        secrets = self.secrets
        return psycopg2Connect(
            host=secrets.pg.host,
            port=secrets.pg.port,
            user=secrets.pg.user,
            password=secrets.pg.password,
            database=secrets.pg.database
        )

    def getInvVariable(self, variable: str) -> str:
        variable = getenv(variable)

        if variable is None:
            raise ValueError(f"Variable {variable} is not set")

        return variable


