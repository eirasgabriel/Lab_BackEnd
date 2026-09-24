# Primeira interface web do Sistema de Gestão de Tarefas (Django)

## Como executar
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Abra http://127.0.0.1:8000/

## Rotas
| URL | View | Resposta |
|---|---|---|
| `/` | `inicio` | template `inicio.html` |
| `/tarefas/` | `lista_tarefas` | template `lista.html` |
| `/tarefas/pendentes/` | `tarefas_pendentes` | `lista.html` filtrado |
| `/sobre/` | `sobre` | `HttpResponse` (texto) |

## Fluxo
Navegador → `gestao_tarefas/urls.py` → `tarefas/urls.py` → `views.py` → template → resposta

## Testes
```bash
python manage.py test
```
