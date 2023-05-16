from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUserModel,MobileNumber,Payments

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUserModel
    list_display=['username','email','mobile','is_staff']
    fieldsets = UserAdmin.fieldsets +  (('Extra details',{
        "fields":['mobile','status','photo','wallet','display_name','verified','bio'],
    }),
    )
class MobileNumberAdmin(admin.ModelAdmin):
    list_display = ['mobile','user','verified']



admin.site.register(CustomUserModel,CustomUserAdmin)
admin.site.register(MobileNumber,MobileNumberAdmin)
admin.site.register(Payments)

