from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserModel(AbstractUser):
    mobile = PhoneNumberField(blank=True,default=None,null=True)
    bio = models.CharField(max_length=240,blank=True)
    verified = models.BooleanField(default=False)
    display_name = models.CharField(max_length=20,blank=True,null=True)
    status = models.CharField(max_length=10,default='',blank=True)
    photo = models.ImageField(upload_to='profile pictures/',default='default_user_photo.jpg',blank=True)
    wallet = models.DecimalField(max_digits=20,decimal_places=2,default=0)

    def __str__(self):
        return self.username

class MobileNumber(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    mobile = PhoneNumberField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.mobile)

class Payments(models.Model):
    sender = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='sender')
    recipient = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="recipient")
    amount = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "{} sent {} to {}".format(self.sender,self.amount,self.recipient)

    class Meta:
        verbose_name_plural = 'Payments'
        ordering = ["-created_at"]
    