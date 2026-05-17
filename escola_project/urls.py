"""URLs principais do projeto."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("cursos.urls", "cursos"), namespace="cursos")),
]
