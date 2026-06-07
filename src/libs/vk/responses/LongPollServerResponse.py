class LongPollServerResponse:
    def __init__(self, server: str, key: str, ts: str):
        self.server = server
        self.key = key
        self.ts = ts