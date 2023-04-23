import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.lib.channel_layers.auth_channel_layer import AuthChannelLayer
from chat.lib.channel_layers.message_channel_layer import MessageChannelLayer
from chat.lib.channel_layers.user_channel_layer import UserChannelLayer

from chat.lib.events import EventHandler, EventType, ChannelEvent


class RoomsConsumer(AsyncWebsocketConsumer):

    USER_CHANNEL_METHOD = "user_channel"
    ROOM_CHANNEL_METHOD = "room_channel"

    def __init__(self):
        super().__init__()

        self.event_handler = EventHandler()

        self.auth_layer = AuthChannelLayer(self)
        self.message_layer = MessageChannelLayer(self)
        self.user_layer = UserChannelLayer(self)

        self.event_handler.register_event(EventType.AUTHENTICATE, [self.auth_layer.authenticate, self.user_layer.connected])
        self.event_handler.register_event(EventType.USER_DISCONNECT, self.user_layer.disconnected)

        ####################### MESSAGE EVENTS #######################
        self.event_handler.register_event(EventType.TEXT_MESSAGE, self.message_layer.receive_text)
        self.event_handler.register_event(EventType.IMAGE_MESSAGE, self.message_layer.receive_image)

        self.room_name = None

    def get_access_code(self) -> str:
        return self.scope["url_route"]["kwargs"]["access_code"]

    """
    Our chat room websocket.
    """
    async def connect(self):
        await self.accept()

        access_code = self.scope["url_route"]["kwargs"]["access_code"]
        self.room_name = f"chat_{access_code}"

    async def disconnect(self, close_code):
        await self.event_handler.dispatch(EventType.USER_DISCONNECT, None)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        event: dict = json.loads(text_data)
        print(event)
        event_type = EventType(event["type"])
        data = event["data"]

        await self.event_handler.dispatch(event_type, data)

    # Receive message from room group
    async def message(self, event):
        message = event["data"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type": "message", "data": message}))

    async def user_channel(self, data: dict):
        event = ChannelEvent.deserialize(data)

        # Do not do anything with NO_TRIGGER Events.
        # For more details read docs for NO_TRIGGER_EVENT enum type.
        if event.event_type == EventType.NO_TRIGGER_EVENT:
            return

        print(event.event_type)
        await self.send(json.dumps({
            'type': event.event_type.value,
            'data': event.data
        }))

    async def room_channel(self, data: dict):
        event = ChannelEvent.deserialize(data)

        # Do not do anything with NO_TRIGGER Events.
        # For more details read docs for NO_TRIGGER_EVENT enum type.
        if event.event_type == EventType.NO_TRIGGER_EVENT:
            return

        print(event.event_type)
        await self.send(json.dumps({
            'type': event.event_type.value,
            'data': event.data
        }))
