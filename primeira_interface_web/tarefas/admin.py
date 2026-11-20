"""Registro dos models no Django Admin (Semana 7)."""
from django.contrib import admin

from .models import Categoria, Tarefa

admin.site.register(Categoria)
admin.site.register(Tarefa)
