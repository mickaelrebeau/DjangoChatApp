from django.urls import path
from .views import ChatListView, UserListView, InboxView

app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view(), name='message_list'),
    path('meet/', UserListView.as_view(), name='users_list'),
    path('inbox/<str:username>/', InboxView.as_view(), name='inbox'),
]
