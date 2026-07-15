from src.libs.infra.baseRepository import BaseRepository
from src.domain.messengers.models.response import Response


class ResponseRepository(BaseRepository):
    async def createResponse(
        self, messenger_type: int, request_id: int, data: str, user_uuid: str
    ) -> int:
        sql = """
            INSERT INTO messengers_responses (messenger_type, request_id, data, user_uuid) VALUES ($1, $2, $3, $4)
        """
        async with self.connection() as conn:
            await conn.execute(sql, messenger_type, request_id, data, user_uuid)
            sql = """
                SELECT id FROM messengers_responses WHERE messenger_type = $1 AND request_id = $2 AND user_uuid = $3
            """
            id = await conn.fetchval(sql, messenger_type, request_id, user_uuid)
            if id is None:
                raise Exception("Failed to create response")
            return int(id)

    async def updateResponseUuid(self, response_id: int, response_uuid: str) -> None:
        sql = """
            UPDATE messengers_responses SET response_uuid = $2 WHERE id = $1
        """
        async with self.connection() as conn:
            await conn.execute(sql, response_id, response_uuid)

    async def getResponseByUuid(self, response_uuid: str) -> Response:
        sql = """
            SELECT * FROM messengers_responses WHERE response_uuid = $1
        """
        async with self.connection() as conn:
            response = await conn.fetchrow(sql, response_uuid)
            if response is None:
                raise Exception("Response not found")
            return Response(
                id=response["id"],
                messenger_type=response["messenger_type"],
                request_id=response["request_id"],
                data=response["data"],
                user_uuid=response["user_uuid"],
                response_uuid=response["response_uuid"],
            )
