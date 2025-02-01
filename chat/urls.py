from django.urls import path
from chat.views import (
    UserListView,
    PrivateMessageListView,
    SendMessageView,
    UnreadMessagesView,
    ChatListView,
)

urlpatterns = [
    path("users/", ChatListView.as_view(), name="chat-list"),
    path(
        "messages/<int:receiver_id>/",
        PrivateMessageListView.as_view(),
        name="chat-history",
    ),
    path("messages/send/", SendMessageView.as_view(), name="send-message"),
    path("messages/unread/", UnreadMessagesView.as_view(), name="unread-messages"),
]
