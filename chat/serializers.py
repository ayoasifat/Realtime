from rest_framework import serializers,parsers
from .models import Conversation,Message
from users.serializers import UserDetailsSerializer
 
class MessagesSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField()
    to_user = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserDetailsSerializer(many=True)
    last_message = serializers.SerializerMethodField()

    def get_last_message(self,obj):
        return MessagesSerializer(obj.conversation.first()).data

    class Meta:
        model = Conversation
        fields = '__all__'
        

class MessagesCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False)
    class Meta:
        model = Message
        exclude = ('from_user','to_user','conversation')
        