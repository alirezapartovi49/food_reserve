from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/i18n/", include("django.conf.urls.i18n")),
    path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/accounts/", include("accounts.urls"), name="accounts"),
    path("api/auth/", include("auth.urls"), name="auth"),
    path("api/foods/", include("food.urls"), name="foods"),
    path("api/reserve/", include("reserve.urls"), name="reserves"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
