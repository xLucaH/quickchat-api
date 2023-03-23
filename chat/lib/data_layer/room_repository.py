import uuid
from typing import Union

from quickchat.core import database

from chat.models import Rooms
from chat.lib import utils, domain
from chat.lib.domain import room_models
from chat.lib.domain.room_models import *


class RoomRepository(domain.RoomRepositoryContract, database.DjangoDB):

    def __init__(self):
        super().__init__(use_dict_cursor=True)

        self.room_table = Rooms._meta.db_table
        self.room_users_table = 'chat_room_users'
        self.room_tokens_table = 'chat_room_tokens'

    def get_room_by_access_code(self, access_code: str) -> Union[room_models.RoomModel, None]:
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

        return room_models.RoomModel(
            id=uuid.UUID(data['room_id']),
            name=data['name'],
            access_code=data['access_code'],
            created=data['created'],
            expiring=data['expiring'],
        )

    def get_room_messages(self, room_id: uuid.UUID) -> List[RoomMessageModel]:
        """
        Gets all messages of a given room by its access code.

        :param room_id: Room id (Not the access code).
        :return: A list of all messages of the given room.
        """

        sql_to_execute = """
                         SELECT message_id, created, content, rooms_users__user_id, rooms__room_id
                         FROM chat_messages
                         WHERE rooms__room_id = %s
                         """

        data = self.query(sql_to_execute, (str(room_id), ))

        formatted_data = []

        for row in data:
            formatted_data.append(
                RoomMessageModel(
                    id=uuid.UUID(row['message_id']),
                    created=row['created'],
                    sender_id=uuid.UUID(row['room_users__user_id']),
                    content=row['content'],
                    room_id=uuid.UUID(row["rooms__room_id"])
                )
            )

        return formatted_data

    def get_room_users(self, room_id: uuid.UUID) -> List[RoomUserModel]:
        """
        Gets all joined users that belong to a specific chat room.

        :param room_id: ID of the room to get the users from
        :return: List of joined users
        """

        sql_to_execute = """
                         SELECT user_id, username, ip4, date_joined, last_login, is_active, rooms__room_id,
                                token_id, token, created, expiring, last_modified
                         FROM chat_room_users
                         JOIN chat_room_tokens ON user_id = chat_room_tokens.room_users__user_id
                         WHERE rooms__room_id = %s
                         """

        data = self.query(sql_to_execute, (room_id.hex, ))

        formatted_data = []

        for row in data:
            formatted_data.append(
                RoomUserModel(
                    id=uuid.UUID(row['user_id']),
                    room_id=uuid.UUID(row['rooms__room_id']),
                    username=row['username'],
                    is_active=bool(row['is_active']),
                    date_joined=row['date_joined'],
                    last_login=row['last_login'],
                    ip4=row['ip4'],
                )
            )

        return formatted_data

    def create_room(self, room: room_models.RoomModel) -> room_models.RoomModel:
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

        self.commit()

        return room

    def create_user(self, user: room_models.RoomUserModel) -> room_models.RoomUserModel:
        """
        Adds an existing user by its id to a given room by its id.

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
        })

        self.commit()

        return user

    def create_room_token(self, room_token: room_models.RoomAuthTokenModel) -> room_models.RoomAuthTokenModel:
        """
        Creates a token for a room that can be used to verify an incoming request and make sure the request
        is allowed to access the room's data_layer.
        :param room_token:
        """

        self.insert(self.room_tokens_table, {
            'token_id': room_token.id.hex,
            'token': room_token.value,
            'created': room_token.created,
            'expiring': room_token.expiring,
            'last_modified': utils.now(),
            'room__room_id': room_token.room_id.hex,
            'room_users__user_id': room_token.user_id.hex,
        })

        self.commit()

        return room_token

    def get_room_token(self, token: str) -> Union[RoomAuthTokenModel, None]:

        sql_to_execute = f"""
                         SELECT token_id, token, created, expiring, last_modified, room__room_id,
                                room_users__user_id
                         FROM chat_room_tokens
                         WHERE token = %s
                         """

        token = self.query(sql_to_execute, (token, ), single=True)

        if token is None:
            return None

        return RoomAuthTokenModel(
            id = uuid.UUID(token['token_id']),
            value = token['token'],
            created = token['created'],
            expiring = token['expiring'],
            last_modified = token['last_modified'],
            user_id = uuid.UUID(token['room_users__user_id']),
            room_id = uuid.UUID(token['room__room_id']),
        )

    def get_user_by_id(self, user_id: str) -> Union[RoomUserModel, None]:

        sql_to_execute = """
                         SELECT user_id, username, ip4, date_joined, last_login, is_active, rooms__room_id
                         FROM chat_room_users
                         WHERE user_id = %s
                         """

        row = self.query(sql_to_execute, (user_id, ), single=True)

        if row is None:
            return None

        return RoomUserModel(
            id = uuid.UUID(row['user_id']),
            room_id = uuid.UUID(row['rooms__room_id']),
            username = row['username'],
            is_active = bool(row['is_active']),
            date_joined = row['date_joined'],
            last_login = row['last_login'],
            ip4 = row['ip4'],
        )