from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import uuid

userModel = get_user_model()
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.TextField()
    participants = models.ManyToManyField(userModel, related_name='participants')
    timestamp = models.DateTimeField(auto_now=True,blank=True)
    def __str__(self):
        names = self.name.split('_')
        return 'Conversation between {} and {}'.format(names[0],names[1])
   
    

class Message(models.Model):
    from_user = models.ForeignKey(userModel,on_delete=models.CASCADE,related_name='from_user')
    to_user = models.ForeignKey(userModel,on_delete=models.CASCADE,related_name='to')
    content = models.TextField()
    payment = models.DecimalField(max_digits=20,decimal_places=2,default=None,blank=True,null=True)
    picture = models.ImageField(upload_to='photos/',default=None,null=True,blank=True,)
    file = models.FileField(upload_to='files/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    video = models.FileField(upload_to='videos/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    duration = models.DecimalField(max_digits=7,decimal_places=5,default=None,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name='conversation')
    read = models.BooleanField(default=False) 
    def __str__(self):
        return 'Message from {} to {}'.format(self.from_user,self.to_user)
    class Meta:
        ordering = ['-timestamp']

