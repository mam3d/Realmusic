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


class UserUpdateViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("update")
        self.user = UserFactory(username="testuser", password="testing321")
        self.data = {
            "username": "newusername",
            "email": "test@gmail.com",
        }
        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_put(self):
        response = self.client.put(self.url, self.data, **self.authorization_header)
        self.assertEqual(response.status_code, 200)
        
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, "newusername")

        # test user and verification code cached
        self.assertTrue(cache.get(self.user.username))



class EmailChangeViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("email_change")
        self.user = UserFactory(username="testuser", password="testing321")
        self.payload = {
            "code":1234,
        }
        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    @mock.patch("user.api.serializers.cache.get")
    def test_put(self, mock_object):
        mock_object.return_value = {"email":"s@gmail.com","code":1234}
        response = self.client.put(self.url, self.payload, **self.authorization_header)
        user = User.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.email, "s@gmail.com")


class PasswordResetViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("password_reset")
        self.user = UserFactory(username="testuser", password="mypassword", email="test@gmail.com")
        self.payload = {
            "email":"test@gmail.com",
            "code":1234,
            "new_password":"newpassword",
            "new_password2":"newpassword",
        }
        
    @mock.patch("user.api.serializers.cache.get")
    def test_put(self, mock_object):
        mock_object.return_value = 1234
        # this view is unauthenticated only
        response = self.client.post(self.url, self.payload)
        
        user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.check_password("newpassword"))
        
        
