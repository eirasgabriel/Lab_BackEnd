"""Dados fictícios e idempotentes: repetir o comando não duplica registros."""
from django.core.management.base import BaseCommand
from django.db import transaction
from academico.models import Aluno, Professor, Disciplina, Turma, Matricula

class Command(BaseCommand):
    help = 'Cria dados fictícios sem criar usuários ou senhas.'

    @transaction.atomic
    def handle(self, *args, **options):
        professor, _ = Professor.objects.get_or_create(email='docente@example.com', defaults={'nome': 'Docente Demonstração'})
        disciplina, _ = Disciplina.objects.get_or_create(codigo='BE01', defaults={'nome': 'Laboratório Back End'})
        turma, _ = Turma.objects.get_or_create(codigo='BE-2026-2', defaults={'professor': professor, 'disciplina': disciplina})
        for numero, nome in enumerate(['Ana Exemplo', 'Bruno Exemplo', 'Carla Exemplo'], start=1):
            aluno, _ = Aluno.objects.get_or_create(matricula=f'DEMO{numero}', defaults={'nome': nome, 'email': f'aluno{numero}@example.com'})
            Matricula.objects.get_or_create(aluno=aluno, turma=turma)
        self.stdout.write(self.style.SUCCESS('Dados demonstrativos disponíveis.'))
