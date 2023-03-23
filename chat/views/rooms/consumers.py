import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.lib.events import EventType, EventHandler
from chat.lib import data_layer
from chat.lib.domain.di import room_actions
from chat.lib.domain.room_models import Chat


class RoomsConsumer(WebsocketConsumer):

    def __init__(self):
        super().__init__()

        self.repository = data_layer.RoomRepository()

        self.event_handler = EventHandler()
        self.event_handler.register_event(EventType.AUTHENTICATE, self.authenticate_token)

    """
    Our chat room websocket.
    """
    def connect(self):
        self.accept()

        access_code = self.scope["url_route"]["kwargs"]["access_code"]
        self.room_group_name = f"chat_{access_code}"

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        event: dict = json.loads(text_data)
        print(event)
        event_type: EventType = EventType[event["type"].upper()]
        data = event["data"]

        self.event_handler.dispatch(event_type, data)

    # Receive message from room group
    def message(self, event):
        message = event["data"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"event": "message", "data": message}))

    def authenticate_token(self, data: dict):
        user = room_actions.authenticate(data['token'])

        if user is None:
            return

        async_to_sync(self.channel_layer.group_add)(user.id.hex, self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            user.id.hex, {"type": "user_channel", "data": {'type': EventType.AUTHENTICATE_SUCCESS.value}}
        )

    def user_channel(self, event):
        event_type = EventType[event['data']['type'].upper()]

        if event_type == EventType.AUTHENTICATE_SUCCESS:
            self.send(json.dumps({"event": "message", "data": "SUCCESS"}))