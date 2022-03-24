
from rest_framework import (
    views,
    generics,
    status,
)
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    GoogleSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class GoogleLogin(generics.CreateAPIView):
    serializer_class = GoogleSerializer


class UserLoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
