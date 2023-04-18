import uuid
from datetime import datetime
from dataclasses import dataclass
from typing import List
from enum import Enum

from quickchat.core import helper_classes


class MessageType(Enum):

    TEXT = 0
    IMAGE = 1


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
    is_online: bool

    date_joined: datetime
    last_login: datetime = None

    ip4: str = None

    def to_dict(self) -> dict:
        return {
            "user_id": self.id.hex,
            "username": self.username,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "date_joined": self.date_joined.isoformat(),
            "is_online": self.is_online
        }

@dataclass
class RoomMessageModel:

    id: uuid.UUID
    created: datetime
    sender_id: uuid.UUID
    content: str
    room_id: uuid.UUID
    message_type: MessageType

    def to_dict(self) -> dict:
        return {
            "sender": self.sender_id.hex,
            "content": self.content,
            "sent_date": self.created.isoformat()
        }


@dataclass
class Chat:

    room: RoomModel
    messages: List[RoomMessageModel]
    users: List[RoomUserModel]


@dataclass
class ChatUser(RoomUserModel):

    is_typing: bool = False

    def to_dict(self) -> dict:
        user_info = super().to_dict()
        user_info['is_typing'] = self.is_typing

        return user_info