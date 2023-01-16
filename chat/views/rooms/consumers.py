import json

from channels.generic.websocket import WebsocketConsumer


class RoomsConsumer(WebsocketConsumer):
    """
    Our chat room websocket.
    """

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=json.dumps({"message": str(text_data)}))
