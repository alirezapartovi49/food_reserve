from django.urls import path

from . import views


urlpatterns = [
    path("active-foods/", views.FoodsView.as_view(), name="all-active-foods")
]
