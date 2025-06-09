"""this file is from old project"""

from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core import exceptions

from local_extentions.validations import persian_to_english, ValidationError


User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=120)
    password = serializers.CharField(max_length=30)

    def validate_email(self, value: str):
        validate_email(value=value)

        user = User.objects.filter(email=value)
        if not user.exists():
            raise serializers.ValidationError(_("کاربری با این اطلاعات وجود ندارد"))
        self.user = user
        return value

    def validate_password(self, value: str):
        return validate_password(value)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30)
    password2 = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("email", "fullname", "username", "city", "password2", "password")

    def validate_email(self, email: str):
        errors = dict()
        try:
            validate_email(value=email)
        except ValidationError:
            errors["email"] = [_("فرمت ایمیل درست نیست")]

        if "email" not in errors:
            user = User.objects.filter(email=email).exists()
            if user:
                errors["email"] = [_("ایمیل تکراری است")]

        if errors:
            raise serializers.ValidationError(errors)

        return email

    def validate(self, attrs: dict):
        password: str | None = attrs.get("password")
        password2: str | None = attrs.pop("password2")

        errors = dict()

        if password is None:
            errors["password"] = [_("پسورد نباید خالی باشد")]

        if password != password2:
            errors["password2"] = [_("پسورد ها یکسان نیستند")]

        if password is not None:
            user = User(**attrs)
            try:
                validate_password(
                    password=password, user=user
                )  # check user is exists and password is macth with user
            except exceptions.ValidationError as e:
                errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserRegisterSerializer, self).validate(attrs)


class UserVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=120)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_code(self, value):
        return persian_to_english(number=value)


class ResendVerifyMessageSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=120)


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
