from src.libs.infra.logger import Logger
import os
from datetime import datetime

class VKLogger(Logger):

    def __init__(self, log_file_path: str):
        super().__init__()
        self.log_file_path = log_file_path
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

    def _log(self, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} {level} {message}\n"

        with open(self.log_file_path, 'a') as f:
            f.write(log_message)

    def info(self, message: str):
        self._log("[INF]", message)

    def error(self, message: str):
        self._log("[ERR]", message)
