
from rest_framework import (
    views,
    generics,
    status,
    permissions
)
from rest_framework.response import Response
from .permissions import UnauthenticatedOnly
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    GoogleSerializer,
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    UserUpdateSerializer,
    EmailChangeSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    lookup_field = None
    
    def get_object(self):
        return self.request.user


class EmailChangeView(generics.UpdateAPIView):
    serializer_class = EmailChangeSerializer
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


class PasswordResetRequestView(views.APIView):
    permission_classes = [UnauthenticatedOnly]
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.save()
            return Response(f"verification email has been sent to {email}", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(views.APIView):
    permission_classes = [UnauthenticatedOnly]
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(f"password changed", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(generics.CreateAPIView):
    serializer_class = GoogleSerializer
    permission_classes = [permissions.AllowAny]

