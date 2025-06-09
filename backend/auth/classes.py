"""this file is from old project"""

from typing import Optional, Tuple, ByteString

from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import Token
from rest_framework.request import Request

from .services import get_client_info
from .token import validated_token


class JWTAuth(JWTAuthentication):
    """
    customize token validation
    """

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token, request)

        return self.get_user(validated_token), validated_token

    def get_validated_token(self, raw_token: ByteString, request) -> Token:
        client_info = get_client_info(request)
        messages = []
        try:
            AuthToken = validated_token(raw_token, client_info)
            return AuthToken
        except TokenError as e:
            messages.append(
                {
                    "token_class": AuthToken.__name__,
                    "token_type": AuthToken.token_type,
                    "message": e.args[0],
                }
            )

        raise InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": messages,
            }
        )
