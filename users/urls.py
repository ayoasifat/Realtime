from django.urls import path,re_path
from .views import RegisterView,Pay,UserListView,Add_Cash,VerifyView,LoginView,UserDetailView,LogoutView

urlpatterns = [
    path('signup/',RegisterView.as_view()),
    path('login/',LoginView),
    path('logout/',LogoutView),
    path('verify/',VerifyView),
    path('user/',UserDetailView.as_view()),
    path('payments/<group_name>',Pay),
    path('payments/',Pay),
    path('users/',UserListView),
    path('addcash/',Add_Cash),
]