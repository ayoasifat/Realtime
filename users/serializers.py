from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers,validators
from django.utils.translation import gettext_lazy as _ 
from  phonenumber_field.serializerfields import PhoneNumberField
from .models import Payments
from django.conf import settings
from rest_framework.authtoken.models import Token

UserModel = get_user_model()

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('password','last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions')
        read_only_fields = ('verified','wallet')
        

class PaymentsSerializer(serializers.ModelSerializer):
    sender = UserDetailsSerializer()
    recipient = UserDetailsSerializer()
    class Meta:
        model = Payments
        fields = '__all__'

class UserRegisterSerailizer(serializers.Serializer):
    username = serializers.CharField(validators=[validators.UniqueValidator(queryset=UserModel.objects.all(),message="Username is already taken. Please choose another one",lookup="iexact")])
    mobile = PhoneNumberField(validators=[validators.UniqueValidator(queryset=UserModel.objects.all(),message="This number is already associated with an account")])

    def validate_username(self,value):
        if value.lower() in settings.USERNAMES_BLACKLIST :
                raise serializers.ValidationError("Username cannot be used")
        return value
    def save(self):
        username = self.validated_data.get("username")
        mobile = self.validated_data.get("mobile")
        user = UserModel.objects.create(username=username,mobile=mobile)
        token  = Token.objects.create(user=user)
        user.set_unusable_password()
        user.save()
        return token.key

