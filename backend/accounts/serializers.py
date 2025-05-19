from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Self

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
            "is_active",
            "is_ban",
            "jlast_login",
            "last_login",
        )


class ActivateAccountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5)


class SelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Self
        fields = "__all__"
