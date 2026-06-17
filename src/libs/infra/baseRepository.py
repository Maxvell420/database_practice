from psycopg2.extensions import connection

class BaseRepository:
    # Подумать над абстракцией для db в будущем...
    def __init__(self, db: connection):
        self.db = db