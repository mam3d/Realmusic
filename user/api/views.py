
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
)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class GoogleLogin(generics.CreateAPIView):
    serializer_class = GoogleSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
