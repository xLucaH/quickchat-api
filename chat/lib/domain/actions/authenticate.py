from typing import Union

from chat.lib.domain.contracts import RoomRepositoryContract
from chat.lib.domain.room_models import RoomUserModel


class AuthenticateAction:

    def __init__(self, repository: RoomRepositoryContract):
        self.repository = repository

    def __call__(self, token: str) -> Union[RoomUserModel, None]:
        token = self.repository.get_room_token(token)

        if token is None or not token.is_active():
            return None

        user = self.repository.get_user_by_id(token.user_id.hex)

        if user is None:
            return None

        self.repository.set_online_status(user.id.hex, True)

        return user