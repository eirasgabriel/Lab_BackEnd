# Atividade: APIs com Django e FastAPI
Data: 20/11/2026
Aluno 1 / matrícula: Gabriel Júnior Eiras Veneno / 202423004
Aluno 2 / matrícula: —

> Valores observados com os dois servidores recém-iniciados (listas em memória no estado
> inicial), usando `curl` no terminal. Saídas completas em [EVIDENCIAS.md](EVIDENCIAS.md).

## 1. Consulta inicial
Endereços, códigos HTTP e aluno inicial:

| API | Endereço completo | Código HTTP | Registro inicial |
|---|---|---|---|
| Django | `GET http://127.0.0.1:8000/alunos` | 200 | `[{"id": 1, "nome": "Ana", "curso": "Engenharia de Software"}]` |
| FastAPI | `GET http://127.0.0.1:8001/alunos` | 200 | `[{"id":1,"nome":"Ana","curso":"Engenharia de Software"}]` |

As duas devolvem o mesmo registro inicial. Só muda a formatação do JSON: o Django põe
espaços depois de `:` e `,`, e o FastAPI não.

## 2. Cadastro
JSON enviado, códigos e identificadores recebidos:

JSON enviado às duas APIs (`POST /alunos`, `Content-Type: application/json`):

```json
{"nome": "Bruno", "curso": "Engenharia de Software"}
```

| API | Código HTTP | Resposta (id recebido) |
|---|---|---|
| Django (com cookie `csrftoken` e cabeçalho `X-CSRFToken`) | 201 | `{"id": 2, "nome": "Bruno", "curso": "Engenharia de Software"}` → **id 2** |
| FastAPI | 201 | `{"id":2,"nome":"Bruno","curso":"Engenharia de Software"}` → **id 2** |

Nova consulta (`GET /alunos`, 200 nas duas): cada lista passou de 1 para 2 registros, com
Bruno (id 2) depois de Ana (id 1). As listas são independentes: cada API só recebeu o
próprio cadastro.

## 3. Validação
JSON inválido, códigos, mensagens e efeito na listagem:

JSON enviado às duas APIs:

```json
{"nome": "   ", "curso": "Engenharia de Software"}
```

| API | Código HTTP | Mensagem |
|---|---|---|
| Django | **400** | `{"erro": "Nome e curso devem ser textos nao vazios."}` |
| FastAPI | **422** | `{"detail":[{"type":"string_too_short","loc":["body","nome"],"msg":"String should have at least 1 character","input":"   ","ctx":{"min_length":1}}]}` |

Efeito na listagem: nenhum. A nova consulta continuou com 2 registros (Ana e Bruno) nas duas
APIs; o nome só com espaços não foi incluído.

## 4. Código
Para cada framework, indicar arquivo, função/classe e trecho curto:

**Django**
- Rota: `django_api/config/urls.py`, lista `urlpatterns`:
  `urlpatterns = [path('alunos', alunos_view)]`. Liga `/alunos` à função `alunos_view`
  (`django_api/alunos/views.py`), que trata GET e POST (`@require_http_methods(['GET', 'POST'])`).
- Validação: `django_api/alunos/views.py`, função `validar`:
  `if not isinstance(valor, str) or not valor.strip(): return None`. `"   ".strip()` é
  vazio, então `validar` devolve `None` e a view responde
  `JsonResponse({'erro': 'Nome e curso devem ser textos nao vazios.'}, status=400)`. Esse é
  o 400 do item 3.
- Resposta: `django_api/alunos/views.py`, função `alunos_view`:
  `alunos.append(aluno)` seguido de `return JsonResponse(aluno, status=201)`. Esse é o 201
  com o aluno do item 2. O id vem de `'id': len(alunos) + 1`. No GET:
  `return JsonResponse(alunos, safe=False)` (200 do item 1).

**FastAPI**
- Rota: `fastapi_api/main.py`, decoradores `@app.get('/alunos')` sobre `listar_alunos` e
  `@app.post('/alunos', status_code=201)` sobre `cadastrar_aluno`.
- Validação: `fastapi_api/main.py`, definição `Texto` e classe `AlunoEntrada`:
  `Texto = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1)]`
  e `nome: Texto`. O Pydantic remove os espaços e o texto fica com 0 caracteres, menor que
  `min_length=1`. O FastAPI responde 422 com `string_too_short` antes de chamar
  `cadastrar_aluno` (item 3).
- Resposta: `fastapi_api/main.py`, função `cadastrar_aluno`: `alunos.append(aluno)` e
  `return aluno`. O código 201 vem de `status_code=201` no decorador (item 2). No GET,
  `listar_alunos` faz `return alunos` (200 do item 1).
