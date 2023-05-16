from rest_framework.generics import ListAPIView,ListCreateAPIView,CreateAPIView
from django.db.models import Q
from .models import Conversation,Message
from .serializers import ConversationSerializer,MessagesSerializer,MessagesCreateSerializer
from .pagination import Pagination
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

userModel = get_user_model()
class ConversationsView(ListAPIView):
    '''List all the current user conversations'''
    serializer_class = ConversationSerializer
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

class MessagesView(ListCreateAPIView):
    '''List all the messages between the current user and the <user> from (api/messages/<user>/)'''
    serializer_class = MessagesSerializer
    pagination_class = Pagination
    def get_queryset(self):
        user = self.kwargs['user']
        return Message.objects.filter(Q(Q(from_user=self.request.user) & Q(to_user=userModel.objects.get(username__iexact=user))) | Q(Q(from_user=userModel.objects.get(username__iexact=user)) & Q(to_user=self.request.user)))


@api_view(['GET'])
def MessagesReadView(request,user):
    '''All <user> from (api/messages/read/<user>/) messages sent to the current user are marked as read'''
    queryset =  Message.objects.filter(Q(from_user = userModel.objects.get(username__iexact=user)) & Q(to_user = request.user))
    queryset.update(read=True) 
    return Response(data={'result':'success'},status=200)

class MessagesCreateView(CreateAPIView):
    '''Create a message object between user1 and user2 from (api/messages/create/user1_user2/) '''
    serializer_class = MessagesCreateSerializer
    queryset = Message.objects.all()

    def get_receiver(self):
        usernames = self.kwargs['group_name'].split('_')
        for username in usernames:
            if username.lower() != self.request.user.username.lower():
                return userModel.objects.get(username__iexact=username)
                
    def perform_create(self, serializer):
        conversation,create = Conversation.objects.get_or_create(name=self.kwargs['group_name'])
        serializer.save(from_user=self.request.user,to_user=self.get_receiver(),conversation=conversation)




        
