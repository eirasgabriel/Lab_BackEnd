"""Views: recebem a requisição, preparam os dados e devolvem uma resposta."""
from django.http import HttpResponse
from django.shortcuts import render

# Dados EM MEMÓRIA (o banco de dados com models chega nas próximas semanas).
TAREFAS = [
    {"id": 1, "titulo": "Configurar ambiente virtual", "prioridade": "Alta", "situacao": "Concluída"},
    {"id": 2, "titulo": "Criar rotas com urls.py", "prioridade": "Alta", "situacao": "Pendente"},
    {"id": 3, "titulo": "Montar template da lista", "prioridade": "Média", "situacao": "Pendente"},
    {"id": 4, "titulo": "Escrever README", "prioridade": "Baixa", "situacao": "Concluída"},
]


def inicio(request):
    return render(request, "tarefas/inicio.html", {"total": len(TAREFAS)})


def lista_tarefas(request):
    contexto = {"titulo_pagina": "Todas as tarefas", "tarefas": TAREFAS}
    return render(request, "tarefas/lista.html", contexto)


def tarefas_pendentes(request):
    pendentes = [t for t in TAREFAS if t["situacao"] == "Pendente"]
    contexto = {"titulo_pagina": "Tarefas pendentes", "tarefas": pendentes}
    return render(request, "tarefas/lista.html", contexto)


def sobre(request):
    # HttpResponse devolve texto simples, útil para testar uma rota rapidamente
    return HttpResponse("Sistema de Gestão de Tarefas — Laboratório de Programação Back End")
