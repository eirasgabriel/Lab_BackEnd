"""ModelForm reaproveita campos, tipos e validações do Model."""
from django import forms
from .models import Aluno, Professor, Disciplina, Turma, Matricula

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'email']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'email']

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'codigo']

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['codigo', 'disciplina', 'professor', 'semestre']

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['aluno', 'turma', 'nota1', 'nota2']
