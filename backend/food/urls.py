from django.urls import path

from . import views


urlpatterns = [path("week-foods", views.FoodsView.as_view(), name="week-foods")]
