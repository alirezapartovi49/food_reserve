from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r"selfs", views.SelfViewSet, basename="selfs")

urlpatterns = [
    path("profile/", views.UserProfileAPIView.as_view(), name="profile"),
    path(
        "activate_account/", views.ActivateAccountView.as_view(), name="active-account"
    ),
    path("delete_account/", views.DeleteAccountView.as_view(), name="delete-account"),
    path("", include(router.urls)),
]
