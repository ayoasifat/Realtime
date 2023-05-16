from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import PaymentsSerializer,UserRegisterSerailizer,UserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .verify import send,check
from .models import MobileNumber,Payments
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework.authtoken.models import Token
from chat.models import Conversation,Message
from chat.serializers import MessagesSerializer

userModel = get_user_model()
@permission_classes([AllowAny])
class RegisterView(CreateAPIView):
    '''Create a new user. An unusable password is set as the user password'''
    serializer_class = UserRegisterSerailizer    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response({"token":token})


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def VerifyView(request):
    '''Verifies a user token\n Parameters : mobile,token'''
    if request.method == 'POST':
        result = check(request.data.get('mobile'),request.data.get('token'))
        if(result):
            try:
                user =userModel.objects.get(mobile=request.data.get('mobile'))
                token,created = Token.objects.get_or_create(user=user)
                return Response({"detail":"Success","token":token.key,"user":UserDetailsSerializer(user).data},status=200)
            except:
                return Response({"detail":"New User"},status=201)
        else:
            return Response({'detail':'failed'},status=404)
    return Response('Type a token')

@api_view(['GET','POST'])
def Pay(request,group_name=""):
    '''POST : Sends payments between users\n GET :Gets all current user transactions \n Parameters: recipient_id,amount'''
    if request.method == "POST":
        user = request.user
        recipient = userModel.objects.get(id=request.data.get('recipient_id'))
        amount = int(request.data.get('amount'))
        if user.wallet >= amount:
            user.wallet -= amount
            user.save()
            recipient.wallet += amount
            recipient.save()
            conversation = Conversation.objects.get(name=group_name)
            message = Message.objects.create(from_user=user,to_user=recipient,payment=amount,conversation=conversation,content="payment")
            Payments.objects.create(sender=user,recipient=recipient,amount=amount)
            return Response(MessagesSerializer(message).data)
        else :
            return Response({'detail':'Insufficient Funds'},status=404)
    elif request.method == "GET":
        payments = Payments.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        serializer = PaymentsSerializer(payments,many=True)
        
        return Response(serializer.data)

@api_view(["POST"])
def Add_Cash(request):
    '''Adds cash to the current user wallet \n Parameters:amount'''
    user = request.user
    amount = request.data.get("amount")
    user.wallet += int(amount)
    user.save()
    return Response({"detail":"Success"},status=200)


@api_view(['GET'])
def UserListView(request):
    '''Query parameters: a comma separated string of numbers
    The phonenumbers should be uriencoded i.e %2B = +  and + = space'''
    mobile = request.query_params.get('mobile')
    if mobile:
        mobile_numbers = mobile.split(',')
        users = []
        for mobile_number in mobile_numbers:
            try:
                user = userModel.objects.get(mobile=mobile_number)
                serializer = UserDetailsSerializer(user)
                users.append(serializer.data)
            except:
                pass
        return Response(users)
    else :
        users = userModel.objects.all()
        serializer = UserDetailsSerializer(users,many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def LoginView(request):
    '''Sends a verification code to the provided number \n Parameters:mobile'''
    mobile = request.data.get('mobile')
    try:
        user = userModel.objects.get(mobile=mobile)
        if not user.is_active:
            return Response({"detail":"This account has been suspended"},status=404)
    except:
        pass
    send(mobile)
    return Response({"detail":"A Verification code was sent to {}".format(mobile)})


class UserDetailView(RetrieveUpdateDestroyAPIView):
    '''Returns details about the current user. User details can be updated through this endpoint.'''
    serializer_class = UserDetailsSerializer
    def get_object(self):
        return userModel.objects.get(username=self.request.user.username)

@api_view(['GET'])
def LogoutView(request):
    '''logs out the current user (Destroys the user's token)'''
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
    except:
        return Response({"detail":"Not authenticated"}, status=404)
    return Response({"detail":"Success"})

