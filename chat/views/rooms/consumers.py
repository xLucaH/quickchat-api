import json

from channels.generic.websocket import WebsocketConsumer

from chat.lib.channel_layers.auth_channel_layer import AuthChannelLayer
from chat.lib.channel_layers.message_channel_layer import MessageChannelLayer

from chat.lib.events import EventHandler, EventType, ChannelEvent


class RoomsConsumer(WebsocketConsumer):

    def __init__(self):
        super().__init__()

        self.event_handler = EventHandler()

        self.auth_layer = AuthChannelLayer(self)
        self.message_layer = MessageChannelLayer(self)

        self.event_handler.register_event(EventType.AUTHENTICATE, self.auth_layer.authenticate)
        self.event_handler.register_event(EventType.MESSAGES, self.message_layer.receive)

    def get_access_code(self) -> str:
        return self.scope["url_route"]["kwargs"]["access_code"]

    """
    Our chat room websocket.
    """
    def connect(self):
        self.accept()

        access_code = self.scope["url_route"]["kwargs"]["access_code"]
        room_group_name = f"chat_{access_code}"

    def disconnect(self, close_code):
        pass
        # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        event: dict = json.loads(text_data)
        print(event)
        event_type = EventType(event["type"])
        data = event["data"]

        self.event_handler.dispatch(event_type, data)

    # Receive message from room group
    def message(self, event):
        message = event["data"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": "message", "data": message}))

    def user_channel(self, data: dict):
        event = ChannelEvent.deserialize(data)
        self.send(json.dumps({
            'type': event.event_type.value,
            'data': event.data
        }))

    def room_channel(self, data: dict):
        event = ChannelEvent.deserialize(data)
        self.send(json.dumps({
            'type': event.event_type.value,
            'data': event.data
        }))
