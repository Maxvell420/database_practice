from src.libs.infra.baseRepository import BaseRepository
from src.domain.messengers.models.request import Request
from src.domain.messengers.enums.messangerTypes import MessangerTypes


class RequestRepository(BaseRepository):
    async def createRequest(
        self, messenger_type: int, data: str, user_uuid: str, request_uuid: str
    ) -> int:
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

    async def getRequestByUuid(
        self, request_uuid: str, messenger_type: MessangerTypes
    ) -> Request:
        sql = """
            SELECT * FROM messengers_requests WHERE request_uuid = $1 AND messenger_type = $2
        """
        async with self.connection() as conn:
            request = await conn.fetchrow(sql, request_uuid, messenger_type.value)
            if request is None:
                raise Exception("Request not found")
            return Request(
                id=request["id"],
                messenger_type=request["messenger_type"],
                data=request["data"],
                user_uuid=request["user_uuid"],
                request_uuid=request["request_uuid"],
            )
