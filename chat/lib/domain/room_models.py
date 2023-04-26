import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import List
from enum import Enum

from chat.lib.domain.files.media_folder import build_media_url
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
class RoomMessageAttachmentModel:

    id: uuid.UUID
    message_id: uuid.UUID

    path: str
    mime_type: str

    def to_dict(self) -> dict:
        return {
            "url": build_media_url(self.path),
            "mime_type": self.mime_type
        }


@dataclass
class RoomMessageModel:

    id: uuid.UUID
    created: datetime
    sender_id: uuid.UUID
    content: str
    room_id: uuid.UUID
    message_type: MessageType
    attachments: List[RoomMessageAttachmentModel] = field(default_factory=lambda: [])

    def to_dict(self) -> dict:
        return {
            "sender": self.sender_id.hex,
            "text": self.content,
            "sent_date": self.created.isoformat(),
            'type': self.message_type.value,
            'attachments': [x.to_dict() for x in self.attachments],
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