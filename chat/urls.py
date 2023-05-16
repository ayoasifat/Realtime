from django.urls import path
from .views import ConversationsView,MessagesView,MessagesReadView,MessagesCreateView
urlpatterns = [
    path('conversations/',ConversationsView.as_view()),
    path('messages/<user>/',MessagesView.as_view()),
    path('messages/read/<user>',MessagesReadView),
    path('messages/create/<group_name>',MessagesCreateView.as_view()),
]