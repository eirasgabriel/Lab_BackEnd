"""As classes descrevem tabelas; objetos representam registros dessas tabelas."""
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField()

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.matricula})'

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

class Turma(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT)
    semestre = models.CharField(max_length=6, default='2026.2')

    def __str__(self):
        return f'{self.codigo} - {self.disciplina.nome}'

class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT, related_name="matriculas")
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    # None significa nota ainda não lançada; zero é uma nota válida.
    nota1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    nota2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['aluno', 'turma'], name='aluno_turma_unicos'),
            models.CheckConstraint(condition=models.Q(nota1__isnull=True) | models.Q(nota1__gte=0, nota1__lte=10), name='nota1_valida'),
            models.CheckConstraint(condition=models.Q(nota2__isnull=True) | models.Q(nota2__gte=0, nota2__lte=10), name='nota2_valida'),
        ]

    @property
    def media(self):
        if self.nota1 is None or self.nota2 is None:
            return None
        return (self.nota1 + self.nota2) / Decimal('2')

    @property
    def situacao(self):
        # Regra apenas didática: não representa o regulamento institucional.
        if self.media is None:
            return 'Pendente'
        return 'Aprovado' if self.media >= Decimal('6') else 'Reprovado'

    def __str__(self):
        return f'{self.aluno.nome} / {self.turma.codigo}'

