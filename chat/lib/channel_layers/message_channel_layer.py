from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from chat.lib.domain.room_models import RoomUserModel
from chat.lib.events import EventType, ChannelEvent


class MessageChannelLayer:

    def __init__(self, ws: WebsocketConsumer):

        self.ws = ws

    def receive(self, message: str):
        channel_layer = get_channel_layer()
        user: RoomUserModel = self.ws.scope['user']

        room_data_event = ChannelEvent(
            method="room_channel",
            event_type=EventType.MESSAGES,
            data = {
                "text": message,
                "sent": datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                "userId": user.id.hex
            }
        )

        async_to_sync(channel_layer.group_send)(
            f"chat_{self.ws.get_access_code()}", room_data_event.serialize()
        )