
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
            is_staff=True,
            is_admin=True,
            is_superuser=True,
            )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username