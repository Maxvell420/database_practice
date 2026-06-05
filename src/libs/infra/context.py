from .allocator import Allocator
from .secrets import Secrets
from psycopg2.extensions import connection

class Context:

    def __init__(self, allocator: Allocator):
        self.allocator = allocator
    
    @property
    def secrets(self) -> Secrets:
        return self.allocator.secrets
    
    @property
    def pgDb(self) -> connection:
        return self.allocator.pgDb