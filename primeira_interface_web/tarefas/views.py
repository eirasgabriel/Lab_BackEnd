"""Views: recebem a requisição, consultam o banco e devolvem uma resposta."""
from django.http import HttpResponse
from django.shortcuts import render

from .models import Tarefa


def inicio(request):
    return render(request, "tarefas/inicio.html", {"total": Tarefa.objects.count()})


def lista_tarefas(request):
    # select_related busca a categoria na mesma consulta, evitando uma
    # consulta extra por tarefa quando o template exibe tarefa.categoria.
    tarefas = Tarefa.objects.select_related("categoria").order_by("data_prevista")
    contexto = {"titulo_pagina": "Todas as tarefas", "tarefas": tarefas}
    return render(request, "tarefas/lista.html", contexto)


def tarefas_pendentes(request):
    pendentes = (
        Tarefa.objects.select_related("categoria")
        .filter(situacao=Tarefa.Situacao.PENDENTE)
        .order_by("data_prevista")
    )
    contexto = {"titulo_pagina": "Tarefas pendentes", "tarefas": pendentes}
    return render(request, "tarefas/lista.html", contexto)


def sobre(request):
    # HttpResponse devolve texto simples, útil para testar uma rota rapidamente
    return HttpResponse("Sistema de Gestão de Tarefas — Laboratório de Programação Back End")
