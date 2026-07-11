from src.libs.infra.logger import Logger
import os
from datetime import datetime
import aiofiles
class VKLogger(Logger):

    def __init__(self, log_file_path: str):
        super().__init__()
        self.log_file_path = log_file_path
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

    async def _log(self, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if message.endswith(("\n", "\r")):
            message = message.rstrip("\r\n")
        log_message = f"{timestamp} {level} {message}\n"

        async with aiofiles.open(self.log_file_path, 'a') as f:
            await f.write(log_message)

    async def info(self, message: str):
        await self._log("[INF]", message)

    async def error(self, message: str):
        await self._log("[ERR]", message)
