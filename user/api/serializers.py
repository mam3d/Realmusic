from django.contrib.auth import authenticate
from rest_framework import serializers
from utils.refresh_token import get_tokens_for_user
from user.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2"]

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("password is to short")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("passwords didn't match")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tokens = get_tokens_for_user(instance)
        ret.update(**tokens)
        return ret


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"wrong credentials":"password or username is incorrect"})
        tokens = get_tokens_for_user(user)
        return tokens
