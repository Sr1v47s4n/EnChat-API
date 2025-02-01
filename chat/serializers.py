from rest_framework import serializers
from chat.models import PrivateMessage
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    content = serializers.CharField(write_only=True)

    class Meta:
        model = PrivateMessage
        fields = ["id", "sender", "receiver", "content", "timestamp", "is_read"]

    def create(self, validated_data):
        sender = self.context["request"].user
        receiver = validated_data.pop("receiver")
        content = validated_data.pop("content")

        return PrivateMessage.objects.create(
            sender=sender, receiver=receiver, encrypted_message=content
        )
