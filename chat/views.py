from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from chat.models import PrivateMessage
from chat.serializers import PrivateMessageSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Max
from utils import decrypt_message  # Import decryption function


User = get_user_model()


class ChatListView(ListAPIView):
    """Retrieve all unique chats of the user with the latest message"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get latest message per conversation
        latest_messages = (
            (
                PrivateMessage.objects.filter(sender=user)
                | PrivateMessage.objects.filter(receiver=user)
            )
            .values("sender", "receiver")
            .annotate(last_msg=Max("timestamp"))
        )

        # Build chat list
        chat_list = []
        seen_users = set()  # To avoid duplicate entries

        for chat in latest_messages:
            last_msg = PrivateMessage.objects.filter(
                sender_id__in=[chat["sender"], chat["receiver"]],
                receiver_id__in=[chat["sender"], chat["receiver"]],
                timestamp=chat["last_msg"],
            ).first()

            if last_msg:
                chat_partner = (
                    last_msg.receiver if last_msg.sender == user else last_msg.sender
                )

                # Ensure unique chat entries
                if chat_partner.id not in seen_users:
                    seen_users.add(chat_partner.id)
                    chat_list.append(
                        {
                            "chat_with": chat_partner.username,
                            "chat_with_id": chat_partner.id,
                            "last_message": decrypt_message(last_msg.encrypted_message),
                            "timestamp": last_msg.timestamp,
                            "is_read": last_msg.is_read,
                        }
                    )

        return Response(chat_list)


class UserListView(ListAPIView):
    """Fetch all users except the logged-in user"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class PrivateMessageListView(ListAPIView):
    """Fetch chat history between two users"""

    serializer_class = PrivateMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        receiver_id = self.kwargs["receiver_id"]
        return PrivateMessage.objects.filter(
            sender=self.request.user, receiver_id=receiver_id
        ) | PrivateMessage.objects.filter(
            sender_id=receiver_id, receiver=self.request.user
        ).order_by(
            "timestamp"
        )


class UnreadMessagesView(APIView):
    """Get unread messages for the logged-in user"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_messages = PrivateMessage.objects.filter(
            receiver=request.user, is_read=False
        )
        response_data = []

        for msg in unread_messages:
            response_data.append(
                {
                    "id": msg.id,
                    "sender": msg.sender.username,
                    "message": msg.get_message(),
                    "timestamp": str(msg.timestamp),
                }
            )
            msg.is_read = True
            msg.save()

        return Response(response_data)


class SendMessageView(CreateAPIView):
    """Send a new private message"""

    serializer_class = PrivateMessageSerializer
    permission_classes = [IsAuthenticated]
