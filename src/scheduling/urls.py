from django.contrib import admin
from django.urls import include, path
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema = get_schema_view(
    Info(title="Scheduling", default_version="v1"),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", schema.with_ui("swagger", cache_timeout=0)),
    path("", include("procedures.urls")),
]
