from typing import List

from chat.lib.domain.contracts import RoomRepositoryContract
from chat.lib.domain.room_models import RoomUserModel


class DisconnectUser:

    def __init__(self, repository: RoomRepositoryContract):

        self.repository = repository

    def __call__(self, user: RoomUserModel):
        self.repository.set_online_status(user.id.hex, False)
        user.is_online = False
