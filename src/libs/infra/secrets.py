from .parts.pg import PGParts
from .parts.vk import VKParts

class Secrets:
    def __init__(self, pg: PGParts | None = None, vk: VKParts | None = None):
        self.pg: PGParts | None = pg
        self.vk: VKParts | None = vk