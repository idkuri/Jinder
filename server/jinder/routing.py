from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"web-socket/chat", consumers.chat_consumer.as_asgi()),
]
