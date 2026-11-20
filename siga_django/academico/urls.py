from django.urls import path
from . import views
urlpatterns = [
    path('', views.painel, name='painel'),
    path('<str:entidade>/', views.listar, name='listar'),
    path('<str:entidade>/novo/', views.salvar, name='criar'),
    path('<str:entidade>/<int:pk>/editar/', views.salvar, name='editar'),
    path('<str:entidade>/<int:pk>/excluir/', views.excluir, name='excluir'),
]
