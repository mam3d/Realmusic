from unittest import mock
from rest_framework.test import APITestCase, APIRequestFactory
from user.api.serializers import (
    GoogleSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
    UserUpdateSerializer,
    EmailChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
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


class UserUpdateSerializerTest(APITestCase):

    def setUp(self):
        self.user = UserFactory(username="test", password="testing321")
        self.request = APIRequestFactory()
        self.request.user = self.user
        
    def test_valid(self):
        payload = {
            "username":"newusername",
            "email":"newusername@gmail.com",
        }
        serializer = UserUpdateSerializer(self.user, data=payload, context={"request":self.request})
        self.assertTrue(serializer.is_valid())


class EmailChangeSerializerTest(APITestCase):

    def setUp(self):
        self.user = UserFactory(username="test", password="testing321")
    
    @mock.patch("user.api.serializers.cache")
    def test_valid(self, mock_object):
        mock_object.get.return_value = {"code":1245}
        payload = {
            "code":1245,
        }
        serializer = EmailChangeSerializer(self.user, data=payload)
        self.assertTrue(serializer.is_valid())

    @mock.patch("user.api.serializers.cache")
    def test_not_valid(self, mock_object):
        mock_object.get.return_value = {"code":0000}
        payload = {
            "code":1245,
        }
        serializer = EmailChangeSerializer(self.user, data=payload)
        self.assertFalse(serializer.is_valid())


class PasswordResetRequestSerializerTest(APITestCase):
        
    def test_valid(self):
        UserFactory(username="test", email="valid@gmail.com")
        payload = {
            "email":"valid@gmail.com",
        }
        serializer = PasswordResetRequestSerializer(data=payload)
        self.assertTrue(serializer.is_valid())

    def test_not_valid(self):
        # user with this email dosen't exist
        payload = {
            "email":"notvalid@gmail.com",
        }
        serializer = PasswordResetRequestSerializer(data=payload)
        self.assertFalse(serializer.is_valid())


class PasswordResetSerializerTest(APITestCase):

    def setUp(self):
        self.payload = {
            "email":"valid@gmail.com",
            "code":1212,
            "new_password":"testpass",
            "new_password2":"testpass"
        }
        self.serializer = PasswordResetSerializer(data=self.payload)

    @mock.patch("user.api.serializers.cache")    
    def test_valid(self, mock_object):
        mock_object.get.return_value = 1212
        self.assertTrue(self.serializer.is_valid())

    def test_no_cache_set(self):
        # cache.get isn't mocked so it dosen't exist
        self.assertFalse(self.serializer.is_valid())

    @mock.patch("user.api.serializers.cache") 
    def test_passwords_dont_match(self, mock_object):
        mock_object.get.return_value = 1212
        self.payload["new_password2"] = "something diffrent"
        self.assertFalse(self.serializer.is_valid())

    @mock.patch("user.api.serializers.cache") 
    def test_wrong_code(self, mock_objcet):
        mock_objcet.get.return_value = 555
        self.payload["code"] = 111
        self.assertFalse(self.serializer.is_valid())
