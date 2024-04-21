import json
import uuid

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.views import postChat

class chat_consumer(WebsocketConsumer):
    chat_group_name = "chat_group"
    players = {}

    def connect(self):
        self.player_id = str(uuid.uuid4())
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )
        
        self.send(
            text_data=json.dumps({"type": "connectionStatus", "status": "OK"})
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )

    def receive(self, text_data):
        data_json = json.loads(text_data)
        if data_json["type"] == "postChat":
            async_to_sync(self.channel_layer.group_send)(self.chat_group_name, {"type": "refreshChat"})
            postChat(data_json["username"], data_json["message"])

    def refreshChat(self, event):
        # Handle message event here
        # message = event['message']
        # Do something with the message...
        self.send(json.dumps({"type": "refreshChat"}))

