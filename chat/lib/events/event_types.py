from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventType(Enum):

    AVAILABLE = 'chat.status.available'
    AUTHENTICATE = 'chat.auth.request'
    AUTHENTICATE_SUCCESS = "chat.auth.success"
    TEXT_MESSAGE = "chat.message.text"
    SYSTEM_MESSAGE = "chat.message.system"
    IMAGE_MESSAGE = "chat.message.image"
    VIDEO_MESSAGE = "chat.message.video"
    AUDIO_MESSAGE = "chat.message.audio"
    USERS = "chat.users"
    ROOM = "chat.room"
    TEST_AUTH = "chat.test_auth"
    USER_DISCONNECT = "chat.user.disconnect"

    # This is a hack for a bug that occurs when trying to execute group_send multiple times in a row.
    # Use this event if you encounter this bug.
    # This event won't be sent back to the client.
    NO_TRIGGER_EVENT = "NO_TRIGGER"


@dataclass
class ChannelEvent:

    method: str
    event_type: EventType
    data: Any

    def serialize(self) -> dict:
        return {
            'type': self.method,  # This needs to be 'type'. It maps to a method name in our consumer class.
            'event_type': self.event_type.value,
            'data': self.data
        }

    @staticmethod
    def deserialize(data: dict) -> ChannelEvent:
        return ChannelEvent(
            method=data['type'],
            event_type=EventType(data['event_type']),
            data=data['data']
        )
