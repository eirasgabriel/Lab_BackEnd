"""URLs do PROJETO: encaminham as requisições para as aplicações."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tarefas.urls")),  # delega para tarefas/urls.py
]
