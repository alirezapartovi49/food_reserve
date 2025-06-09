from django.core import exceptions
from rest_framework import serializers
from django.db.utils import IntegrityError
from drf_spectacular.types import OpenApiTypes
from django.core.validators import validate_email
from drf_spectacular.utils import extend_schema_field
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User
from accounts.serializers import UserProfileSerializer
from local_extentions.validations import ValidationError


class UserSerializer(UserProfileSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(
        read_only=True
    )  # use underline for compatibilty with python id func
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["_id", "username", "email", "fullname", "isAdmin"]

    def get_id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    @extend_schema_field(OpenApiTypes.STR)
    def get_fullname(self, obj: User):
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

    def create(self, validated_data: dict):
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
            raise exceptions.BadRequest(_("کاربر تکراری است"))

    @extend_schema_field(OpenApiTypes.STR)
    def get_token(self, obj: User) -> str:
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def validate_email(self, email):
        errors = dict()
        try:
            validate_email(value=email)
        except ValidationError:
            errors["email"] = [_("email validation error")]

        if "email" not in errors:
            user = User.objects.filter(email=email).first()
            if user:
                errors["email"] = [_("این کاربر تکراری است")]

        if errors:
            raise serializers.ValidationError(errors)

        return email

    def validate(self, attrs: dict):
        """
        customizing validate of all serializer data
        its becouse some fields needs validate together and add add some validations of business logic here
        """

        password: str | None = attrs.get("password")
        password2: str | None = attrs.pop("password2")

        errors = dict()

        if password != password2:
            errors["password2"] = [_("پسورد ها بربر نیستند")]

        # this code remove extra fields (like password2) automatically in db level of queries
        if password is not None:
            user = User(**attrs)
            try:
                # validate the password and catch the exception
                validators.validate_password(password=password, user=user)
            # the exception raised here is different than serializers.ValidationError
            except exceptions.ValidationError as e:
                errors["password"] = list(e.messages)

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return super(UserSerializerWithToken, self).validate(attrs)


class CustomizedTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_active:
            raise serializers.ValidationError({"error": _("حساب شما فعال نیست")})

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data
