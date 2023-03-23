from typing import Union
import uuid

from django.http.request import HttpRequest

from quickchat.core import utils as core_utils

from chat.lib import auth, exceptions
from chat.lib.domain.contracts import RoomRepositoryContract
from chat.lib.domain.room_models import RoomUserModel, RoomAuthTokenModel, RoomModel

class JoinRoomAction:

    def __init__(self, repository: RoomRepositoryContract):
        self.repository = repository

    def __call__(self, request: HttpRequest, username: str, access_code: str) -> RoomAuthTokenModel:
        room = self.repository.get_room_by_access_code(access_code)

        if room is None:
            raise exceptions.RoomNotExisting('Room does not exist.')

        user_id = uuid.uuid4()

        self.repository.create_user(
            RoomUserModel(
                id=user_id,
                room_id=room.id,
                username=username,
                date_joined=core_utils.now(),
                is_active=True,
            )
        )

        token = auth.create_user_token(
            ip4=core_utils.get_client_ip(request),
            username=username,
            user_id=user_id,
            room_id=room.id
        )

        self.repository.create_room_token(token)

        return token
