from chat.lib.domain.contracts import RoomRepositoryContract
from chat.lib.domain.room_models import *
from chat.lib import exceptions


class GetRoomAction:

    def __init__(self, repository: RoomRepositoryContract):
        self.repository = repository

    def __call__(self, access_code: str) -> Chat:
        room = self.repository.get_room_by_access_code(access_code)

        if room is None:
            raise exceptions.RoomNotExisting

        messages = self.repository.get_room_messages(room.id)
        users = self.repository.get_room_users(room.id)

        return Chat(
            room=room,
            messages=messages,
            users=users
        )

