import uuid
import bleach
from datetime import datetime
from typing import Union, List

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer


from chat.lib.domain.di import room_actions
from chat.lib.domain.room_models import RoomMessageModel, ChatUser, MessageType
from chat.lib.events import EventType, ChannelEvent

from .channel_methods import ROOM_CHANNEL_METHOD


class MessageChannelLayer:

    def __init__(self, ws: WebsocketConsumer):

        self.ws = ws

    def get_user_from_scope(self) -> Union[ChatUser, None]:
        users: List[ChatUser] = self.ws.scope['users']

        for user in users:
            if user.id.hex == self.ws.scope['user_id']:
                return user

        return None

    async def receive_text(self, data: dict):
        text = data['message']
        allowed_html_tags = ["div", "&nbsp;", "br"]
        channel_layer = get_channel_layer()
        user: ChatUser = self.get_user_from_scope()

        message = RoomMessageModel(
            id=uuid.uuid4(),
            created=datetime.now(),
            sender_id=user.id,
            content=bleach.clean(text, tags=allowed_html_tags), # using bleach library to sanitize the user input.
            room_id=user.room_id,
            message_type=MessageType.TEXT
        )

        room_actions.log_message(message)

        room_data_event = ChannelEvent(
            method=ROOM_CHANNEL_METHOD,
            event_type=EventType.TEXT_MESSAGE,
            data = message.to_dict()
        )

        await channel_layer.group_send(self.ws.room_name, room_data_event.serialize())

    async def receive_image(self, data):
        x = 2