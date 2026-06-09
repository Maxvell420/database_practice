from .update import Update
class UpdatesResponse:
    def __init__(self, ts: int, updates: list[Update]):
        self.ts = ts
        self.updates = updates