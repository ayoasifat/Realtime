from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUserModel

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUserModel
        fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUserModel
        fields = UserChangeForm.Meta.fields