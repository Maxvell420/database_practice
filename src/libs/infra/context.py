from .allocator import Allocator
from .secrets import Secrets
from psycopg2 import connect as psycopg2Connect

class Context:

    def __init__(self, allocator: Allocator):
        self.allocator = allocator
    
    @property
    def secrets(self) -> Secrets:
        return self.allocator.secrets
    
    @property
    def pgDb(self) -> psycopg2Connect:
        return self.allocator.pgDb