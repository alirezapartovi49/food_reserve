from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .user_serializer import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    UserSerializerWithToken,
)
from accounts.models import User


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    serializer_class = UserSerializerWithToken
    model = User

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MyTokenRefreshView(TokenRefreshView):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_active:
            raise ValidationError({"error": "حساب شما فعال نیست"})

        return data


@api_view(["POST"])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            fullname=data["fullname"],
            username=data["username"],
            email=data["email"],
            password=make_password(data["password"]),
        )

        serializer = UserSerializerWithToken(user, many=False)
        for i in serializer.data:
            print(i, type(i))
        return Response(
            data={
                "username": serializer.data["username"],
                "id": serializer.data["id"],
                "email": serializer.data["email"],
                "token": serializer.data["token"],
            }
        )
    except Exception as e:
        message = {"detail": str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
