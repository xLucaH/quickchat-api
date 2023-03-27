from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EventType(Enum):

    AUTHENTICATE = 'chat.auth.request'
    AUTHENTICATE_SUCCESS = "chat.auth.success"
    MESSAGES = "chat.message"
    USERS = "chat.users"


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


