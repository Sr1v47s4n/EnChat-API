from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/auth/register/"
        self.login_url = "/auth/login/"

    def test_register_user_success(self):
        """Test successful user registration"""
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password@123",
            "profile_picture": "default_profile_pics/1.png",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_duplicate_user(self):
        """Test duplicate user registration"""
        User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_email(self):
        """Test registration with invalid email"""
        data = {
            "username": "testuser1",
            "email": "invalidemail",
            "password": "password123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """Test successful login"""
        User.objects.create_user(
            username="testuser1", email="testuser1@example.com", password="Password@123"
        )
        data = {"email": "testuser1@example.com", "password": "Password@123"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())

    def test_login_invalid_password(self):
        """Test login with incorrect password"""
        User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        data = {"email": "testuser@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        """Clean up database after each test"""
        User.objects.filter(username="testuser").delete()
