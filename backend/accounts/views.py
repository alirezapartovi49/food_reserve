from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView

from local_extentions.permisions import IsActiveUser, IsAdminOrReadOnly

from .models import User, VerificationCode, Self
from .serializers import (
    UserProfileSerializer,
    ActivateAccountSerializer,
    SelfSerializer,
)


class UserProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def get_object(self):  # noqa: f2678
        """return user object"""
        return self.request.user

    def get_queryset(self):
        return User.objects.filter(
            pk=self.request.user.id,  # auto mapping pk to id
            is_active=True,
            is_ban=False,
        )


class SelfViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Self's routes with IsAdminOrReadOnly permision
    it has update delete and get actions
    """

    serializer_class = SelfSerializer
    permission_classes = (
        IsActiveUser,
        IsAdminOrReadOnly,
    )

    def get_queryset(self):
        return Self.objects.filter(is_active=True)


class ActivateAccountView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivateAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code: str = serializer.validated_data["code"]
        user = request.user
        return self.check_code(user, code)

    def check_code(self, user: User, code: str):
        verification_code = VerificationCode.objects.filter(
            user=user, code=code, is_used=False
        ).first()
        if verification_code:
            verification_code.is_used = True
            verification_code.save()
            user.is_active = True
            user.save()
            return Response(
                {"message": _("حساب شما فعال شد")}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": _("کد فعال سازی اشتباه است")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteAccountView(DestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        IsActiveUser,
    )

    def destroy(self, request, *args, **kwargs):
        instance: User = request.user
        user = User.objects.filter(id=instance.id)
        user_status = user.delete()
        if user_status[0] == 1:  # check user is deleted successfully
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
