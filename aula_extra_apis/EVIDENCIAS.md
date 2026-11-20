# Evidências — Aula extra: APIs com Django e FastAPI

Executado em 20/11/2026, Windows 10. As saídas abaixo são cópias das saídas reais.

## Ambiente

Preparado com o script do professor, sem alterações (`scripts/preparar.py`). Como não há
o comando `py` nesta máquina, ele foi chamado com o executável do Python 3.14 pelo caminho
completo. A saída final do script foi:

```text
3.14.10 (main, Nov 11 2026, 00:19:45) [MSC v.1944 64 bit (AMD64)]
Django 6.0.10 FastAPI 0.165.0 Pydantic 2.14.4 Uvicorn 0.54.0
Ambiente pronto. Execute as tarefas 2 e 3 em terminais separados.
```

| Componente | Versão |
|---|---|
| Python | 3.14.10 |
| Django | 6.0.10 |
| FastAPI | 0.165.0 |
| Pydantic | 2.14.4 |
| Uvicorn | 0.54.0 |

Servidores iniciados com os mesmos comandos das tarefas do VS Code:

```text
.venv\Scripts\python.exe django_api/manage.py runserver 127.0.0.1:8000 --noreload
.venv\Scripts\python.exe -m uvicorn main:app --app-dir fastapi_api --host 127.0.0.1 --port 8001
```

## Itens 1 a 3 (curl, servidores recém-iniciados)

O token CSRF aparece como `<token>`: é o valor do cookie `csrftoken` obtido no primeiro
`GET` ao Django.

```text
### Item 1 — consulta inicial
$ curl http://127.0.0.1:8000/alunos
[{"id": 1, "nome": "Ana", "curso": "Engenharia de Software"}]
[HTTP 200]

$ curl http://127.0.0.1:8001/alunos
[{"id":1,"nome":"Ana","curso":"Engenharia de Software"}]
[HTTP 200]

### Item 2 — cadastro
$ curl -c cookies.txt -b cookies.txt http://127.0.0.1:8000/alunos   (obtém o cookie csrftoken)
[HTTP 200]
(token CSRF obtido do cookie csrftoken; 32 caracteres)

$ curl -b cookies.txt -H 'Content-Type: application/json' -H 'X-CSRFToken: <token>' -X POST -d '{"nome": "Bruno", "curso": "Engenharia de Software"}' http://127.0.0.1:8000/alunos
{"id": 2, "nome": "Bruno", "curso": "Engenharia de Software"}
[HTTP 201]

$ curl -H 'Content-Type: application/json' -X POST -d '{"nome": "Bruno", "curso": "Engenharia de Software"}' http://127.0.0.1:8001/alunos
{"id":2,"nome":"Bruno","curso":"Engenharia de Software"}
[HTTP 201]

$ curl http://127.0.0.1:8000/alunos
[{"id": 1, "nome": "Ana", "curso": "Engenharia de Software"}, {"id": 2, "nome": "Bruno", "curso": "Engenharia de Software"}]
[HTTP 200]

$ curl http://127.0.0.1:8001/alunos
[{"id":1,"nome":"Ana","curso":"Engenharia de Software"},{"id":2,"nome":"Bruno","curso":"Engenharia de Software"}]
[HTTP 200]

### Item 3 — nome só com espaços
$ curl -b cookies.txt -H 'Content-Type: application/json' -H 'X-CSRFToken: <token>' -X POST -d '{"nome": "   ", "curso": "Engenharia de Software"}' http://127.0.0.1:8000/alunos
{"erro": "Nome e curso devem ser textos nao vazios."}
[HTTP 400]

$ curl -H 'Content-Type: application/json' -X POST -d '{"nome": "   ", "curso": "Engenharia de Software"}' http://127.0.0.1:8001/alunos
{"detail":[{"type":"string_too_short","loc":["body","nome"],"msg":"String should have at least 1 character","input":"   ","ctx":{"min_length":1}}]}
[HTTP 422]

$ curl http://127.0.0.1:8000/alunos
[{"id": 1, "nome": "Ana", "curso": "Engenharia de Software"}, {"id": 2, "nome": "Bruno", "curso": "Engenharia de Software"}]
[HTTP 200]

$ curl http://127.0.0.1:8001/alunos
[{"id":1,"nome":"Ana","curso":"Engenharia de Software"},{"id":2,"nome":"Bruno","curso":"Engenharia de Software"}]
[HTTP 200]

### Controle: POST no Django sem token CSRF
$ curl -H 'Content-Type: application/json' -X POST -d '{"nome": "Sem Token", "curso": "Engenharia de Software"}' http://127.0.0.1:8000/alunos
[HTTP 403]
```

Para facilitar a leitura, as opções de formatação do `curl` (`-s`, `-w`) e os caminhos
completos do arquivo de cookies foram tirados das linhas de comando. As respostas não foram
alteradas.

Log do Django nessa execução:

```text
[20/Nov/2026 08:46:07] "GET /alunos HTTP/1.1" 200 61
[20/Nov/2026 08:46:07] "GET /alunos HTTP/1.1" 200 61
[20/Nov/2026 08:46:07] "GET /alunos HTTP/1.1" 200 61
Forbidden (CSRF token from the 'X-Csrftoken' HTTP header has incorrect length.): /alunos
[20/Nov/2026 08:46:08] "POST /alunos HTTP/1.1" 403 2549
[20/Nov/2026 08:46:08] "POST /alunos HTTP/1.1" 201 61
[20/Nov/2026 08:46:08] "GET /alunos HTTP/1.1" 200 124
Bad Request: /alunos
[20/Nov/2026 08:46:08] "POST /alunos HTTP/1.1" 400 53
[20/Nov/2026 08:46:08] "GET /alunos HTTP/1.1" 200 124
Forbidden (CSRF cookie not set.): /alunos
[20/Nov/2026 08:46:08] "POST /alunos HTTP/1.1" 403 2855
```

**Requisição a mais (erro meu no roteiro):** o primeiro `POST ... 403` do log veio de uma
linha do meu roteiro que enviou ao Django o texto literal `$TOKEN` no cabeçalho
`X-CSRFToken`, em vez do token. O Django recusou (`incorrect length`) e nada foi incluído:
o POST seguinte, com o token correto, recebeu o id 2. O último 403 é o controle intencional,
sem cookie e sem token.

Log do FastAPI nessa execução:

```text
INFO:     Started server process [7008]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     127.0.0.1:63786 - "GET /alunos HTTP/1.1" 200 OK
INFO:     127.0.0.1:63788 - "GET /alunos HTTP/1.1" 200 OK
INFO:     127.0.0.1:63792 - "POST /alunos HTTP/1.1" 201 Created
INFO:     127.0.0.1:63794 - "GET /alunos HTTP/1.1" 200 OK
INFO:     127.0.0.1:63796 - "POST /alunos HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:63798 - "GET /alunos HTTP/1.1" 200 OK
```

## Teste automático (`scripts/testar_apis.py`)

Os dois servidores foram encerrados e iniciados de novo antes deste teste, para que as
listas voltassem a ter só Ana.

```text
$ .venv\Scripts\python.exe scripts/testar_apis.py
GET 8000 200 [{"id": 1, "nome": "Ana", "curso": "Engenharia de Software"}]
POST 8000 201 {"id": 2, "nome": "Teste", "curso": "Backend"}
GET 8000 200 [{"id": 1, "nome": "Ana", "curso": "Engenharia de Software"}, {"id": 2, "nome": "Teste", "curso": "Backend"}]
POST 8000 400 {"erro": "Nome e curso devem ser textos nao vazios."}
GET 8000 200 [{"id": 1, "nome": "Ana", "curso": "Engenharia de Software"}, {"id": 2, "nome": "Teste", "curso": "Backend"}]
GET 8001 200 [{"id":1,"nome":"Ana","curso":"Engenharia de Software"}]
POST 8001 201 {"id":2,"nome":"Teste","curso":"Backend"}
GET 8001 200 [{"id":1,"nome":"Ana","curso":"Engenharia de Software"},{"id":2,"nome":"Teste","curso":"Backend"}]
POST 8001 422 {"detail":[{"type":"string_too_short","loc":["body","nome"],"msg":"String should have at least 1 character","input":"   ","ctx":{"min_length":1}}]}
GET 8001 200 [{"id":1,"nome":"Ana","curso":"Engenharia de Software"},{"id":2,"nome":"Teste","curso":"Backend"}]
Verificações concluídas. O teste incluiu um aluno em cada servidor.
```

Código de saída: 0. Ao final os dois servidores foram encerrados; nenhum processo ficou
escutando nas portas 8000 e 8001.

## Não verificado

- A documentação interativa do FastAPI (`/docs`, etapa 5 do README) e a visualização no
  navegador não foram usadas. Todas as requisições foram feitas pelo terminal.
- `scripts/testar.ps1` não foi colado em um terminal PowerShell. O teste equivalente foi
  feito com `curl` e `scripts/testar_apis.py`.
- As tarefas do VS Code (`.vscode/tasks.json`) não foram acionadas pela interface. Os
  comandos que elas executam foram rodados diretamente.
