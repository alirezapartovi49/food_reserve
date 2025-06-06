from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter(trailing_slash=False)
router.register(r"reserve", views.ReserveViewSet, basename="reserves")


urlpatterns = [
    path("", include(router.urls)),
    path("today", views.TodayView.as_view(), name="today-reserves"),
]
