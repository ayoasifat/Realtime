from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from urllib.parse import parse_qs
from rest_framework.authtoken.models import Token
from  .models import Message,Conversation
from django.contrib.auth import get_user_model


userModel = get_user_model()
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        query_params = parse_qs(self.scope["query_string"].decode())['token'][0]
        token = Token.objects.prefetch_related('user').get(key=query_params)
        self.user = token.user
        if (token):
            self.conversation_name = self.scope["url_route"]["kwargs"]["group_name"]
            self.conversation,create = Conversation.objects.get_or_create(name=self.conversation_name)
            self.conversation.participants.set([self.user,self.get_receiver()])
            async_to_sync(self.channel_layer.group_add)(self.conversation_name,self.channel_name)
            self.accept()
        
    def disconnect(self,code):
        async_to_sync(self.channel_layer.group_discard)(
            self.conversation_name, self.channel_name
        )

    def receive(self, text_data):
        text_data = json.loads(text_data)
        type = text_data.get('type')
        if (type=="payment"):
            amount = text_data['amount']
            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name, {"type": "payment","from_user":self.user.username,"payment":amount})
        elif (type=="file"):
            file = text_data['file']
            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name, {"type": "file","from_user":self.user.username,"file":file})
        elif (type=="video"):
            video = text_data['video']
            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name, {"type": "video","from_user":self.user.username,"video":video})
        elif (type=="picture"):
            photo = text_data['picture']
            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name, {"type": "picture","from_user":self.user.username,"picture":photo})
        else:
            message = text_data['message']
            Message.objects.create(from_user=self.user,to_user=self.get_receiver(),content=message,conversation=self.conversation) 
            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name, {"type": "chat_message","from_user":self.user.username,"content": message})

    def get_receiver(self):
        usernames = self.conversation_name.split('_')
        for username in usernames:
            if username.lower() != self.user.username.lower():
                return userModel.objects.get(username__iexact=username)

    def chat_message(self,e): 
        self.send(text_data=json.dumps(e))

    def payment(self,e):
        self.send(text_data=json.dumps(e))

    def file(self,e):
        self.send(text_data=json.dumps(e))

    def picture(self,e):
        self.send(text_data=json.dumps(e))

    def video(self,e):
        self.send(text_data=json.dumps(e))
     
        