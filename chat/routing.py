import django
django.setup()
from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns =  [path('ws/chat/<group_name>/',ChatConsumer.as_asgi())]

