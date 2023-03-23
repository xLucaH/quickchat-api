import uuid
from datetime import datetime
from dataclasses import dataclass
from typing import List

from quickchat.core import helper_classes


@dataclass
class RoomModel(helper_classes.MappingDataclass):

    id: uuid.UUID
    name: str
    access_code: str

    created: datetime
    expiring: datetime

    @property
    def url(self) -> str:
        return f'rooms/{self.access_code}/'


@dataclass
class RoomAuthTokenModel:

    id: uuid.UUID
    value: str
    created: datetime
    expiring: datetime
    last_modified: datetime

    user_id: uuid.UUID
    room_id: uuid.UUID

    def is_active(self) -> bool:
        now = datetime.now()

        if now > self.expiring:
            return False

        return True


@dataclass
class RoomUserModel(helper_classes.MappingDataclass):

    id: uuid.UUID
    room_id: uuid.UUID

    username: str
    is_active: bool
    date_joined: datetime

    last_login: datetime = None
    ip4: str = None


@dataclass
class RoomMessageModel:

    id: uuid.UUID
    created: datetime
    sender_id: uuid.UUID
    content: str
    room_id: uuid.UUID


@dataclass
class Chat:

    room: RoomModel
    messages: List[RoomMessageModel]
    users: List[RoomUserModel]
