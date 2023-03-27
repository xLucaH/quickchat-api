from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from chat.lib.domain.di import room_actions
from chat.lib.events import EventType, ChannelEvent


class AuthChannelLayer:

    USER_CHANNEL_METHOD = "user_channel"
    ROOM_CHANNEL_METHOD = "room_channel"

    def __init__(self, websocket: WebsocketConsumer):
        self.websocket = websocket

    def authenticate(self, data: dict):
        token = data['token']
        user = room_actions.authenticate(token)

        if user is None:
            self.websocket.disconnect("NOT_AUTHENTICATED")
            return

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_add)(user.id.hex, self.websocket.channel_name)

        chat = room_actions.get_chat(user.room_id.hex, by_id=True)

        async_to_sync(channel_layer.group_add)(f"chat_{chat.room.access_code}", self.websocket.channel_name)

        channel_auth_event = ChannelEvent(
            method=self.USER_CHANNEL_METHOD,
            event_type=EventType.AUTHENTICATE_SUCCESS,
            data= user.to_dict()
        )

        channel_users_event = ChannelEvent(
            method=self.USER_CHANNEL_METHOD,
            event_type=EventType.USERS,
            data = [x.to_dict() for x in chat.users]
        )

        async_to_sync(channel_layer.group_send)(
            user.id.hex, channel_auth_event.serialize()
        )

        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.room.access_code}", channel_users_event.serialize()
        )

        self.websocket.scope['user'] = user
