from os import getenv
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection

from .parts.pg import PGParts
from .secrets import Secrets
from .parts.vk import VKParts


load_dotenv()
class Allocator:
    def __init__(self):
        self._secrets: Secrets | None = None
        self._pg_db: connection | None = None

    @property
    def secrets(self) -> Secrets:
        if self._secrets is None:
            self._secrets = self.loadSecrets()
        return self._secrets

    @property
    def pgDb(self) -> connection:
        if self._pg_db is None:
            self._pg_db = self.loadPgDb()
        return self._pg_db

    def loadSecrets(self) -> Secrets:
        return Secrets(pg=self.loadPgParts(), vk=self.loadVkParts())

    def loadPgParts(self) -> PGParts:
        # подумать в будущем как лучше сделать это
        return PGParts(
            host=self.getInvVariable('DB1_HOST'),
            port=int(self.getInvVariable('DB1_PORT')),
            user=self.getInvVariable('DB1_USER'),
            password=self.getInvVariable('DB1_PASSWORD'),
            database=self.getInvVariable('DB1_DATABASE')
        )

    def loadVkParts(self) -> VKParts:
        return VKParts(
            token=self.getInvVariable('VK_TOKEN'),
            group_id=int(self.getInvVariable('GROUP_ID'))
        )

    def loadPgDb(self) -> connection:
        secrets = self.secrets
        return connect(
            host=secrets.pg.host,
            port=secrets.pg.port,
            user=secrets.pg.user,
            password=secrets.pg.password,
            database=secrets.pg.database
        )

    def getInvVariable(self, variable: str) -> str:
        envVariable = getenv(variable)

        if envVariable is None:
            raise ValueError(f"Variable {variable} is not set")

        return envVariable


