
from rest_framework import (
    views,
    generics,
    status,
    permissions
)
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    GoogleSerializer,
    PasswordChangeSerializer,
    UserUpdateSerializer,
)
from ..models import User


class UserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    lookup_field = None
    
    def get_object(self):
        return self.request.user


class UserLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(views.APIView):
    def post(self, request):
        serializer = PasswordChangeSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("password changed", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(generics.CreateAPIView):
    serializer_class = GoogleSerializer
    permission_classes = [permissions.AllowAny]

