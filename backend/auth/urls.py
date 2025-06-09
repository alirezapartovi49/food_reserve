from django.urls import path

from . import user_views as views


app_name = "auth"


urlpatterns = [  # this field for old project
    # path("login/", views.UserLoginView.as_view()),
    # path("register/", views.UserRegisterView.as_view()),
    # path("verify/", views.UserVerifyView.as_view()),
    # path("verify/resend/", views.ResendVerifyMessage.as_view()),
    # path("token/refresh/", views.JwtRefreshView.as_view()),
    # path("token/verify/", views.JwtVerifyView.as_view()),
    # path("logout/", views.UserLogoutView.as_view()),
]

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.CustomizedTokenObtainPairView.as_view(), name="login"),
    path("refresh", views.CustomizedTokenRefreshView.as_view(), name="token_refresh"),
]
