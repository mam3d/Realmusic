from unittest import mock
from rest_framework import serializers
from rest_framework.test import APITestCase
from user.api.serializers import (
    GoogleSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
)
from .factory import UserFactory

class RegisterSerializerTest(APITestCase):

    def setUp(self):
        self.data = {
            "username":"mam3d",
            "password":"testing321",
            "password2":"testing321"
        }

    def test_valid(self):
        serializer = RegisterSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), True)

    def test_not_valid(self):
        self.data["password2"] = "diffrent"
        serializer = RegisterSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)

    def test_user_exists(self):
        user = UserFactory()
        self.data["username"] = user.username
        serializer = RegisterSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)


class LoginSerializerTest(APITestCase):

    def setUp(self):
        self.data = {
            "username":"mam3d",
            "password":"testing321",
        }

    def test_valid(self):
        user = UserFactory(username="mam3d", password="testing321")
        serializer = LoginSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), True)

    def test_not_valid(self):
        # user dosent exist
        serializer = LoginSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)


class GoogleSerializerTest(APITestCase):

    def setUp(self):
        self.data = {
            "token":"somerandomtokenfortest"
        }
        self.status_code = 200
        
    def get_mock(self, url, **kwargs):
        response = mock.Mock()
        response.status_code = self.status_code
        response.json.return_value = {
            "email":"test@gmail.com"
        }
        return response

    @mock.patch("user.api.serializers.requests")
    def test_valid(self, mock_requests):
        mock_requests.get.side_effect = self.get_mock

        serializer = GoogleSerializer(data=self.data) 
        self.assertEqual(serializer.is_valid(), True)

    @mock.patch("user.api.serializers.requests")
    def test_not_valid(self, mock_requests):
        self.status_code = 400
        mock_requests.get.side_effect = self.get_mock
        
        serializer = GoogleSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())


class PasswordChangeSerializerTest(APITestCase):

    def setUp(self):
        self.user = UserFactory(username="test", password="testing321")
        
    def test_valid(self):
        payload = {
            "current_password":"testing321",
            "new_password":"newpass111",
            "new_password2":"newpass111",
        }
        serializer = PasswordChangeSerializer(self.user, data=payload)
        self.assertTrue(serializer.is_valid())

    def test_not_valid(self):
        # wrong current password
        payload = {
            "current_password":"testing",
            "new_password":"newpass111",
            "new_password2":"newpass111",
        }
        serializer = PasswordChangeSerializer(self.user, data=payload)
        self.assertFalse(serializer.is_valid())

        # new passwords dont match
        payload = {
            "current_password":"testing321",
            "new_password":"newpass",
            "new_password2":"newpass111",
        }
        serializer = PasswordChangeSerializer(self.user, data=payload)
        self.assertFalse(serializer.is_valid())