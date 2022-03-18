
from rest_framework import serializers
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
    