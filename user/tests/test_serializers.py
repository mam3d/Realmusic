
from rest_framework.test import APITestCase
from user.api.serializers import (
    RegisterSerializer,
    LoginSerializer
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
