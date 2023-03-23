import uuid
from typing import Union
from datetime import datetime
from dataclasses import dataclass

from chat.lib.auth import RoomAuthTokenModel
from quickchat.core import database, helper_classes
from chat.models import Rooms
from chat.lib import utils


@dataclass
class RoomModel(helper_classes.MappingDataclass):

    id: uuid.UUID
    name: str
    access_code: str

    created: datetime
    expiring: datetime


@dataclass
class RoomUserModel(helper_classes.MappingDataclass):

    id: uuid.UUID
    room_id: uuid.UUID
    token_id: uuid.UUID

    username: str
    is_active: bool
    date_joined: datetime

    last_login: datetime = None
    ip4: str = None


class Query(database.DjangoDB):

    def __init__(self):
        super().__init__(use_dict_cursor=True)

        self.room_table = Rooms._meta.db_table
        self.room_users_table = 'chat_room_users'
        self.room_tokens_table = 'chat_room_tokens'

    def get_room_by_access_code(self, access_code: str) -> Union[RoomModel, None]:
        """
        Find's a room by its id inside the database and returns a RoomModel instance.
        If no room was found, None is returned.

        :param access_code: the room to find
        """
        sql_to_execute = f"""
                         SELECT room_id, name, access_code, created, expiring
                         FROM {self.room_table}
                         WHERE access_code = %s
                         """

        data = self.query(sql_to_execute, (access_code, ), single=True)

        if not data:
            return None

        return RoomModel(
            id=uuid.UUID(data['room_id']),
            name=data['name'],
            access_code=data['access_code'],
            created=data['created'],
            expiring=data['expiring'],
        )

    def create_room(self, room: RoomModel) -> RoomModel:
        """
        Creates a new room from a given RoomModel inside the database.

        :param room: RoomModel dataclass
        """

        self.insert(self.room_table, {
            'room_id': room.id.hex,
            'name': room.name,
            'access_code': room.access_code,
            'created': room.created.strftime('%Y-%m-%d %H:%M:%S'),
            'expiring': room.expiring.strftime('%Y-%m-%d %H:%M:%S')
        })

        return room

    def create_room_user(self, user: RoomUserModel) -> RoomUserModel:
        """
        Add's an existing user by it's id to a given room by it's id.

        :param user:
        """

        self.insert(self.room_users_table, {
            'user_id': user.id.hex,
            'username': user.username,
            'ip4': user.ip4,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'is_active': user.is_active,
            'rooms__room_id': user.room_id.hex,
            'room_tokens__token_id': user.token_id.hex
        })

        return user

    def create_room_token(self, room_token: RoomAuthTokenModel) -> RoomAuthTokenModel:
        """
        Creates a token for a room that can be used to verify an incoming request and make sure the request
        is allowed to access the room's data_layer.
        :param room_token:
        """

        self.insert(self.room_tokens_table, {
            'token_id': room_token.id.hex,
            'token': room_token.token,
            'created': room_token.created,
            'expiring': room_token.expiring,
            'last_modified': utils.now(),
            'room_users__user_id': room_token.user_id.hex
        })

        return room_token

    def validate_room_token(self, token: str) -> bool:

        sql_to_execute = f"""
                         SELECT COUNT(user_id) as has_token FROM {self.room_tokens_table}
                         LEFT JOIN chat_room_users ON token_id = room_tokens__token_id
                         WHERE token = %s
                         """

        has_token = self.query(sql_to_execute, (token, ))[0]['has_token']

        return True if has_token == 1 else False
