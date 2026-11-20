from django.urls import path
from alunos.views import alunos_view
urlpatterns = [path('alunos', alunos_view)]
