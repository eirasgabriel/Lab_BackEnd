"""URLs da APLICAÇÃO tarefas (arquivo criado manualmente)."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("tarefas/", views.lista_tarefas, name="lista_tarefas"),
    path("tarefas/pendentes/", views.tarefas_pendentes, name="tarefas_pendentes"),
    path("sobre/", views.sobre, name="sobre"),
]
