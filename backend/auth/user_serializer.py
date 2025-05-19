from django.core import exceptions
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.utils import IntegrityError

from accounts.models import User
from accounts.serializers import UserProfileSerializer
from local_extentions.validations import validate_email, ValidationError


class UserSerializer(UserProfileSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "_id", "username", "email", "fullname", "isAdmin"]

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    @extend_schema_field(OpenApiTypes.STR)
    def get_fullname(self, obj):
        name = obj.fullname
        if name == "":
            name = str(obj.email).split("@")[0]

        return name


class UserSerializerWithToken(UserSerializer):
    password2 = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password2",
            "fullname",
            "token",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        try:
            validated_data.pop("password2")
        except KeyError:
            pass
        try:
            user = User(is_active=True, **validated_data)
            user.set_password(password)
            user.save()
            return user
        except IntegrityError:
            raise exceptions.BadRequest("integrity error")

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def validate_email(self, email):
        errors = dict()
        try:
            validate_email(email=email)
        except ValidationError:
            errors["email"] = [_("email validation error")]

        if "email" not in errors:
            user = User.objects.filter(email=email).first()
            if user:
                errors["email"] = [_("the user with this info already exists")]

        if errors:
            raise serializers.ValidationError(errors)

        return email

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it

        # get the password from the data
        password = data.get("password")
        password2 = data.pop("password2")

        errors = dict()

        if password != password2:
            errors["password2"] = [_("passwords must be match")]

        # cp_data = data.copy()
        # cp_data.pop("password2")
        user = User(**data)
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializerWithToken, self).validate(data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # if not self.user.is_active:
        #     raise serializers.ValidationError({"error": "حساب شما فعال نیست"})

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data
