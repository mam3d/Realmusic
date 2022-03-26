
from django.contrib.auth import authenticate
import requests
from rest_framework import serializers
from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("passwords didn't match")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        return user

    def to_representation(self, instance):
        # returning jwt token after user has been created
        token = instance.get_jwt_token()
        return token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"wrong credentials":"password or username is incorrect"})
        return user.get_jwt_token()

class GoogleSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate_token(self, value):
        params = {"access_token": value}
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=params)
        if r.status_code != 200:
            raise serializers.ValidationError("wrong access_token")
        return r.json()["email"]

    def create(self, validated_data):
        # email returned from validate_token()
        email = validated_data["token"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email)
        return user

    def to_representation(self, instance):
        return instance.get_jwt_token()