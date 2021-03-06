
import requests
from django.core.validators import MinLengthValidator
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework import serializers
from user.models import User
from utils.email import Email


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2"]

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("password should be atleast 8 characters")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"error":"password's didn't match"})
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
            raise serializers.ValidationError({"error":"password or username is incorrect"})
        return user.get_jwt_token()

class GoogleSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate_token(self, value):
        params = {"access_token": value}
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=params)
        if r.status_code != 200:
            raise serializers.ValidationError({"error":"wrong access_token"})
        return r.json()["email"]

    def create(self, validated_data):
        # email returned from validate_token()
        email = validated_data["token"]
        user, created = User.objects.get_or_create(email=email)
        return user

    def to_representation(self, instance):
        return instance.get_jwt_token()


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate_current_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError("this is not your current password")
        return value

    def validate(self, data):
        if data.get("new_password") != data.get("new_password2"):
            raise serializers.ValidationError({"error":"passwords don't match"})

        if data.get("new_password") == data.get("current_password"):
            raise serializers.ValidationError({"error":"new password and current password cant be the same"})
        
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]
        extra_kwargs = {
            "username":{"required":False}
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if value != user.email:
            email = Email(value, user=user)
            email = email.send()
            return email


    def to_representation(self, instance):
        data =  super().to_representation(instance)
        email = self.validated_data.get("email")
        if email:
            data["email"] = f"verification code has been sent to {email}"
        return data

    def update(self, instance, validated_data):
        validated_data.pop("email", None)
        return super().update(instance, validated_data)


class EmailChangeSerializer(serializers.Serializer):
    code = serializers.IntegerField()

    def validate(self, validated_data):
        user = self.instance
        data = cache.get(user.username)
        if data:
            if data.get("code") != validated_data["code"]:
                raise serializers.ValidationError({"code":"wrong code"})
            return data # return cached data
        raise serializers.ValidationError({"error":"you must first request verification email"})
    
    def to_representation(self, instance):
        return {
            "user": instance.username,
            "email":instance.email,
            }

    def update(self, instance, validated_data):
        email = validated_data["email"]
        instance.email = email
        instance.save()
        cache.delete(instance.username)
        return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user.exists():
            return value
        else:
            raise serializers.ValidationError("user with this email dosen't exist")

    def save(self, **kwargs):
        # send verification email to posted email
        email = Email(self.validated_data["email"])
        email = email.send()
        return email


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()
    new_password = serializers.CharField(validators=[MinLengthValidator(8)])
    new_password2 = serializers.CharField(validators=[MinLengthValidator(8)])

    def validate(self, data):
        code = cache.get(data["email"])
        if not code:
            raise serializers.ValidationError({"error":"you must request verification email first"})
        if data["new_password"] != data["new_password2"]:
            raise serializers.ValidationError({"error":"passwords don't match"})
        if code != data["code"]:
            raise serializers.ValidationError({"error":"wrong code"})
        return data


    def save(self, **kwargs):
        password = self.validated_data["new_password"]
        user = User.objects.get(email=self.validated_data["email"])
        user.set_password(password)
        user.save()
        