"""Models: classes que descrevem os dados persistidos no banco (Semana 7)."""
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    # TextChoices padroniza os valores gravados no banco (ex.: "ALTA") e
    # oferece um rótulo legível para exibição (ex.: "Alta").
    class Prioridade(models.TextChoices):
        BAIXA = "BAIXA", "Baixa"
        MEDIA = "MEDIA", "Média"
        ALTA = "ALTA", "Alta"

    class Situacao(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        CONCLUIDA = "CONCLUIDA", "Concluída"

    titulo = models.CharField(max_length=150)
    # blank=True: a descrição é opcional no Admin e em formulários.
    descricao = models.TextField(blank=True)
    prioridade = models.CharField(
        max_length=10,
        choices=Prioridade.choices,
        default=Prioridade.MEDIA,
    )
    data_prevista = models.DateField()
    situacao = models.CharField(
        max_length=10,
        choices=Situacao.choices,
        default=Situacao.PENDENTE,
    )
    # PROTECT impede excluir uma categoria que ainda tem tarefas associadas,
    # evitando tarefas sem classificação.
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.titulo
