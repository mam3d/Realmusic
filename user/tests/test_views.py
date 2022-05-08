from unittest import mock
from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.cache import cache
from user.models import User
from .factory import UserFactory

class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.data = {
            "username": "test",
            "password": "password",
            "password2": "password",
        }
    def test_post(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("access" in response.data)


class UserLoginViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("login")
        user = UserFactory(username="testuser", password="testing321")
        self.data = {
            "username": "testuser",
            "password": "testing321",
        }

    def test_post(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)


class GoogleLoginViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("google_login")
        self.data = {
            "token":"somerandomtokenfortest"
        }
        
    def get_mock(self, url, **kwargs):
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {
            "email":"test@gmail.com"
        }
        return response

    @mock.patch("user.api.serializers.requests")
    def test_valid(self, mock_requests):
        mock_requests.get.side_effect = self.get_mock

        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 201)

class UserUpdateViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("update")
        self.user = UserFactory(username="testuser", password="testing321")
        self.data = {
            "username": "newusername",
            "email": "test@gmail.com",
        }
        access = self.user.get_jwt_token()["access"]
        authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}
        self.response = self.client.put(self.url, self.data, **authorization_header)

    def test_post(self):
        self.assertEqual(self.response.status_code, 200)

    def test_user_updated(self):
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, "newusername")

    def test_email_cached(self):
        self.assertTrue(cache.get(self.user.username))
