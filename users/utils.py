from .models import MobileNumber

def setup_user_mobile(user):
    MobileNumber.objects.create(user=user,mobile=
    user.mobile)
 