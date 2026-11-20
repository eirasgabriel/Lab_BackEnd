from django.contrib import admin
from .models import Aluno, Professor, Disciplina, Turma, Matricula
admin.site.register([Aluno, Professor, Disciplina, Turma, Matricula])
