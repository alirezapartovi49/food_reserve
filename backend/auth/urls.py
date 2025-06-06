from django.urls import path

from . import user_views as views


app_name = "auth"


urlpatterns = [
    # path("login/", views.UserLoginView.as_view()),
    # path("register/", views.UserRegisterView.as_view()),
    # path("verify/", views.UserVerifyView.as_view()),
    # path("verify/resend/", views.ResendVerifyMessage.as_view()),
    # path("token/refresh/", views.JwtRefreshView.as_view()),
    # path("token/verify/", views.JwtVerifyView.as_view()),
    # path("logout/", views.UserLogoutView.as_view()),
]

urlpatterns = [
    path("login", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("refresh", views.MyTokenRefreshView.as_view(), name="token_refresh"),
    # path('profile/', views.getUserProfile, name="users-profile"),
    # path('profile/update/', views.updateUserProfile, name="user-profile-update"),
    # path('', views.getUsers, name="users"),
]
