from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/api/dashboard/", permanent=False)),

    path("admin/", admin.site.urls),

    # Rotas da FinanceAPI
    path("api/", include("finance.urls")),

    # Login pelo site
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    # Logout pelo site
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),

    # Documentação OpenAPI
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),
]