
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegisterView,
    UserLoginView,
    UserUpdateView,
    PasswordChangeView,
    GoogleLogin,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('update/', UserUpdateView.as_view(), name="update"),
    path('password-change/', PasswordChangeView.as_view(), name="password_change"),
    path('google-login/', GoogleLogin.as_view(), name="google_login"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
