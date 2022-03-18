from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
