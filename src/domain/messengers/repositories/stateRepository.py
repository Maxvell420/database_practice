from src.libs.infra.baseRepository import BaseRepository
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.enums.states import States
from src.domain.messengers.models.state import State
from json import loads
from json import dumps


class StateRepository(BaseRepository):
    async def persit(self, state: State) -> None:
        sql = """
            INSERT INTO users_states (user_uid, state, messenger_type, data) VALUES ($1, $2, $3, $4)
        """
        async with self.connection() as conn:
            await conn.execute(
                sql,
                state.user_uid,
                state.state.value,
                state.messenger_type.value,
                dumps(state.data),
            )

    async def deleteStates(self, user_uid: str, messenger_type: MessangerTypes) -> None:
        sql = """
            DELETE FROM users_states WHERE user_uid = $1 AND messenger_type = $2
        """
        async with self.connection() as conn:
            await conn.execute(sql, user_uid, messenger_type.value)

    async def findState(
        self, user_uid: str, messenger_type: MessangerTypes
    ) -> State | None:
        sql = """
            SELECT * FROM users_states WHERE user_uid = $1 AND messenger_type = $2
        """
        async with self.connection() as conn:
            state = await conn.fetchrow(sql, user_uid, messenger_type.value)
            if state is None:
                return None
            data = loads(state["data"])
            return State.model_validate(
                {
                    "user_uid": state["user_uid"],
                    "state": state["state"],
                    "messenger_type": state["messenger_type"],
                    "data": data,
                }
            )
