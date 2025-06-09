from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.generics import CreateAPIView

from .user_serializer import (
    CustomizedTokenObtainPairSerializer,
    UserSerializerWithToken,
)
from local_extentions.permisions import IsActiveUser
from accounts.models import User


class CustomizedTokenObtainPairView(TokenObtainPairView):
    """login view with customized token pair view"""

    serializer_class = CustomizedTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    """validate and create user with obtained data"""

    serializer_class = UserSerializerWithToken
    model = User


class CustomizedTokenRefreshView(TokenRefreshView):
    """create refresh token for active user"""

    def get_permissions(self):
        permisions: list = super().get_permissions()
        permisions.append(IsActiveUser)
        return permisions
