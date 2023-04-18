from chat.lib.domain.contracts import RoomRepositoryContract
from chat.lib.domain.room_models import *
from chat.lib import exceptions


class GetChatAction:

    def __init__(self, repository: RoomRepositoryContract):
        self.repository = repository

    def __call__(
            self,
            access_code: str,
            by_id = True,
            messages_since: datetime = None
    ) -> Chat:

        if by_id:
            get_room_method = self.repository.get_room_by_id
        else:
            get_room_method = self.repository.get_room_by_access_code

        room = get_room_method(access_code)

        if room is None:
            raise exceptions.RoomNotExisting

        messages = self.repository.get_room_messages(room.id, since = messages_since)
        users = self.repository.get_room_users(room.id)

        return Chat(
            room=room,
            messages=messages,
            users=users
        )

