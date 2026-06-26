from src.libs.infra.baseRepository import BaseRepository

class RequestRepository(BaseRepository):
    async def createRequest(self, messenger_type: int, data: str, user_uuid: str, request_uuid: str) -> int:
        sql = """
            INSERT INTO messengers_requests (messenger_type, data, user_uuid, request_uuid) VALUES ($1, $2, $3, $4) RETURNING *
        """
        async with self.connection() as conn:
            await conn.execute(sql, messenger_type, data, user_uuid, request_uuid)
            sql = """
                SELECT id FROM messengers_requests WHERE messenger_type = $1 AND user_uuid = $2 AND request_uuid = $3 ORDER BY created_at DESC LIMIT 1
            """
            id = await conn.fetchval(sql, messenger_type, user_uuid, request_uuid)
            if id is None:
                raise Exception("Failed to create request")
            return int(id)