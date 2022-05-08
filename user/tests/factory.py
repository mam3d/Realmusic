from factory.django import DjangoModelFactory
from user.models import User

class UserFactory(DjangoModelFactory):
    username = "mam3d00"
    password = "testing321"
    email = None
    
    class Meta:
        model = User