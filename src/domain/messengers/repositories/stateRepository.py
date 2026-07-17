from src.libs.infra.baseRepository import BaseRepository
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.enums.states import States
from src.domain.messengers.models.state import State
from json import loads
from json import dumps


class StateRepository(BaseRepository):
    async def createState(
        self,
        user_id: int,
        state: States,
        messenger_type: MessangerTypes,
        data: dict | None = None,
    ) -> None:
        sql = """
            INSERT INTO states (user_id, state, messenger_type, data) VALUES ($1, $2, $3, $4)
        """
        async with self.connection() as conn:
            await conn.execute(
                sql, user_id, state.value, messenger_type.value, dumps(data)
            )

    async def findState(
        self, user_id: int, messenger_type: MessangerTypes
    ) -> State | None:
        sql = """
            SELECT * FROM states WHERE user_id = $1 AND messenger_type = $2
        """
        async with self.connection() as conn:
            state = await conn.fetchrow(sql, user_id, messenger_type.value)
            if state is None:
                return None
            data = loads(state["data"])
            return State.model_validate(
                {
                    "user_id": state["user_id"],
                    "state": state["state"],
                    "messenger_type": state["messenger_type"],
                    "data": data,
                }
            )
