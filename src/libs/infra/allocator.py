from os import getenv
from dotenv import load_dotenv
from .parts.pg import PGParts
from .secrets import Secrets
from .parts.vk import VKParts
from asyncpg.pool import create_pool, Pool
from asyncpg.connection import Connection
load_dotenv()
class Allocator:
    def __init__(self):
        self._secrets: Secrets | None = None
        self._pgDbPool: Pool | None = None

    def secrets(self) -> Secrets:
        if self._secrets is None:
            self._secrets = self.loadSecrets()
        return self._secrets

    async def pgDbPool(self) -> Pool:
        if self._pgDbPool is None:
            self._pgDbPool =await create_pool(
            host=self.secrets().pg.host,
            port=self.secrets().pg.port,
            user=self.secrets().pg.user,
            password=self.secrets().pg.password,
            database=self.secrets().pg.database
        )
        return self._pgDbPool

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

    def getInvVariable(self, variable: str) -> str:
        envVariable = getenv(variable)

        if envVariable is None:
            raise ValueError(f"Variable {variable} is not set")

        return envVariable


