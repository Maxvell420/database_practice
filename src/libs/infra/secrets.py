from .parts.pg import PGParts
from .parts.vk import VKParts

class Secrets:
    def __init__(self, pg: PGParts, vk: VKParts):
        self.pg = pg
        self.vk = vk