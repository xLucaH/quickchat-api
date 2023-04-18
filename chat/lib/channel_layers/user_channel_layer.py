from typing import List, Union

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from chat.lib.channel_layers.channel_methods import ROOM_CHANNEL_METHOD
from chat.lib.domain.room_models import RoomUserModel, ChatUser
from chat.lib.events import EventType, ChannelEvent
from chat.lib.domain.di import room_actions

class UserChannelLayer:

    def __init__(self, ws: WebsocketConsumer):

        self.ws = ws

    def get_user_from_scope(self) -> Union[ChatUser, None]:
        users: List[ChatUser] = self.ws.scope['users']

        for user in users:
            if user.id.hex == self.ws.scope['user_id']:
                return user

        return None

    async def connected(self, data):
        user = self.get_user_from_scope()
        user.is_online = True

        await self.send_users()

    async def disconnected(self, *args, **kwargs):
        user = self.get_user_from_scope()
        room_actions.disconnect_user(user)

        channel_layer = get_channel_layer()

        await channel_layer.group_discard(
            user.id.hex, self.ws.room_name
        )
        await self.send_users()

    async def send_users(self):
        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            self.ws.room_name,
            ChannelEvent(
                method=ROOM_CHANNEL_METHOD,
                event_type=EventType.USERS,
                data=[x.to_dict() for x in self.ws.scope['users']]
            ).serialize()
        )