from django.forms import ValidationError
from rest_framework.test import APITestCase
from user.api.serializers import (
    RegisterSerializer
)

class UserRegisterSerializerTest(APITestCase):

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