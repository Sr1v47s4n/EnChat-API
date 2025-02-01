from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from chat.models import PrivateMessage

User = get_user_model()


class ChatAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.user1 = User.objects.create_user(email="user1@example.com", password="password123", username="user1")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password123", username="user2")
        self.non_existent_user_id = 9999  # ID that does not exist

        # Authenticate user1 for API calls
        self.client.force_authenticate(user=self.user1)

    def test_send_message_success(self):
        """Test sending a valid private message"""
        data = {"receiver": self.user2.id, "content": "Hello, user2!"}
        response = self.client.post("/chat/messages/send/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrivateMessage.objects.count(), 1)

    def test_send_message_invalid_receiver(self):
        """Test sending a message to a non-existent user"""
        data = {"receiver": self.non_existent_user_id, "content": "Hello, user2!"}
        response = self.client.post("/chat/messages/send/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_send_message_empty_content(self):
        """Test sending a message with empty content"""
        data = {"receiver": self.user2.id, "content": ""}
        response = self.client.post("/chat/messages/send/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_send_message_invalid_receiver(self):
        """Test sending a message to a non-existent user"""
        data = {"receiver": self.non_existent_user_id, "content": "Hello, user2!"}
        response = self.client.post("/chat/messages/send/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_send_message_empty_content(self):
        """Test sending a message with empty content"""
        data = {"receiver": self.user2.id, "content": ""}
        response = self.client.post("/chat/messages/send/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_chat_history_success(self):
        """Test fetching chat history between two users"""
        PrivateMessage.objects.create(sender=self.user1, receiver=self.user2, encrypted_message="Hello, user2!")
        response = self.client.get(f"/chat/messages/{self.user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["sender"]["username"], self.user1.username)
        
        
    def test_get_chat_history_invalid_user(self):
        """Test fetching chat history with an invalid user"""
        response = self.client.get(f"/chat/messages/message{self.non_existent_user_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_chat_history_unauthorized_user(self):
        """Test fetching chat history with an unauthorized user"""
        self.client.logout()
        response = self.client.get(f"/chat/messages/{self.user1.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_unread_messages_success(self):
        """Test fetching unread messages for a user"""
        PrivateMessage.objects.create(sender=self.user2, receiver=self.user1, encrypted_message="Hello, user1!", is_read=False)
        response = self.client.get("/chat/messages/unread/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        
        
    def test_get_unread_messages_no_messages(self):
        """Test fetching unread messages when there are none"""
        response = self.client.get("/chat/messages/unread/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
        
  
  
        

        