import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from chat.models import PrivateMessage
from utils import encrypt_message, decrypt_message
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from datetime import datetime
from django.utils.timezone import now

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    return User.objects.filter(id=user_id).first()


@database_sync_to_async
def save_message(sender, receiver, encrypted_message):
    return PrivateMessage.objects.create(
        sender=sender, receiver=receiver, encrypted_message=encrypted_message
    )


@database_sync_to_async
def get_past_messages(sender, receiver):
    messages = PrivateMessage.objects.filter(
        sender_id__in=[sender.id, receiver.id],
        receiver_id__in=[sender.id, receiver.id],
    ).order_by("timestamp")
    return [
        {
            "id": m.id,
            "message": decrypt_message(m.encrypted_message),
            "sender": m.sender.id,
            "receiver": m.receiver.id,
            "timestamp": str(m.timestamp),
            "is_read": m.is_read,
            "read_at": str(m.read_at) if m.read_at else None,
        }
        for m in messages
    ]


@database_sync_to_async
def mark_messages_as_read(receiver, sender):
    unread_messages = PrivateMessage.objects.filter(
        sender=sender, receiver=receiver, is_read=False
    )
    unread_messages.update(is_read=True, read_at=now())
    return list(unread_messages.values("id", "read_at"))


@database_sync_to_async
def update_last_seen(user):
    user.last_seen = now()
    user.save()
    return str(user.last_seen)


@database_sync_to_async
def get_last_seen(user_id):
    user = User.objects.filter(id=user_id).first()
    return str(user.last_seen) if user and user.last_seen else None


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope["user"]

        if not self.sender.is_authenticated:
            await self.close()
            return

        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        self.receiver = await get_user(self.receiver_id)

        if not self.receiver:
            await self.close()
            return

        user_ids = sorted([self.sender.id, self.receiver.id])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        last_seen_time = await update_last_seen(self.sender)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "last_seen_update",
                "user_id": self.sender.id,
                "last_seen": last_seen_time,
            },
        )

        past_messages = await get_past_messages(self.sender, self.receiver)
        await self.send(
            text_data=json.dumps({"type": "past_messages", "messages": past_messages})
        )

        read_messages = await mark_messages_as_read(self.sender, self.receiver)
        if read_messages:
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "read_receipt", "read_messages": read_messages},
            )

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

        await update_last_seen(self.sender)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            if data.get("type") == "mark_as_read":
                read_messages = await mark_messages_as_read(self.sender, self.receiver)
                if read_messages:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {"type": "read_receipt", "read_messages": read_messages},
                    )
                return

            if data.get("type") == "get_last_seen":
                last_seen_time = await get_last_seen(self.receiver.id)
                await self.send(
                    text_data=json.dumps(
                        {"type": "last_seen", "last_seen": last_seen_time}
                    )
                )
                return

            if "message" not in data:
                return

            message = data["message"]
            encrypted_message = encrypt_message(message)

            private_message = await save_message(
                self.sender, self.receiver, encrypted_message
            )

            response = {
                "type": "chat_message",
                "message": message,
                "sender": self.sender.id,
                "receiver": self.receiver.id,
                "timestamp": str(private_message.timestamp),
            }

            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "message": json.dumps(response)},
            )

        except json.JSONDecodeError:
            return

    async def chat_message(self, event):
        await self.send(text_data=event["message"])

    async def read_receipt(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "read_receipt", "read_messages": event["read_messages"]}
            )
        )

    async def last_seen_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "last_seen_update",
                    "user_id": event["user_id"],
                    "last_seen": event["last_seen"],
                }
            )
        )
