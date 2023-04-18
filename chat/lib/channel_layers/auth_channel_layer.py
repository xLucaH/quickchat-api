from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from chat.lib.domain.di import room_actions
from chat.lib.events import EventType, ChannelEvent

from .channel_methods import USER_CHANNEL_METHOD
from ..domain.room_models import ChatUser


class AuthChannelLayer:

    def __init__(self, websocket: WebsocketConsumer):
        self.websocket = websocket

    async def authenticate(self, data: dict):
        token = data['token']
        user = room_actions.authenticate(token)

        if user is None:
            self.websocket.disconnect("NOT_AUTHENTICATED")
            return

        channel_layer = get_channel_layer()

        chat = room_actions.get_chat(user.room_id.hex, by_id=True, messages_since=user.date_joined)
        chat_room_channel = "chat_%s" % chat.room.access_code

        self.websocket.scope['user_id'] = user.id.hex
        self.websocket.scope['users'] = [ChatUser(**x.__dict__) for x in chat.users]

        await channel_layer.group_add(chat_room_channel, self.websocket.channel_name)
        await channel_layer.group_add(user.id.hex, self.websocket.channel_name)

        channel_auth_event = ChannelEvent(
            method=USER_CHANNEL_METHOD,
            event_type=EventType.AUTHENTICATE_SUCCESS,
            data=user.to_dict()
        )
        channel_room_event = ChannelEvent(
            method=USER_CHANNEL_METHOD,
            event_type=EventType.ROOM,
            data = {
                'expiring': chat.room.expiring.isoformat(),
                'name': chat.room.name,
                'messages': [x.to_dict() for x in chat.messages],
            }
        )

        # !!!! CAUTION !!!!
        # I spent days trying to find the reason for why the AUTH_SUCCESS event won't be received from the consumer
        # method.
        # For some reason the first call of the group_send() does not work.
        # So I implemented this shadow event to work around this bug.
        await channel_layer.group_send(
            user.id.hex, ChannelEvent(
                method=USER_CHANNEL_METHOD,
                event_type=EventType.NO_TRIGGER_EVENT,
                data=None
            ).serialize()
        )
        await channel_layer.group_send(
            user.id.hex, channel_auth_event.serialize()
        )
        await channel_layer.group_send(
            user.id.hex, channel_room_event.serialize()
        )
