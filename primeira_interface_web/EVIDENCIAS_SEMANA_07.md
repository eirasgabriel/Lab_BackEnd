# Evidências — Semana 07: persistindo tarefas e categorias com Django

Ambiente: Windows 10, Python 3.15.2, Django 5.2.19, SQLite (`db.sqlite3`, não versionado).
Todos os comandos foram executados a partir de `primeira_interface_web/`. As saídas abaixo
são cópias das saídas reais (sem edição), registradas em 20/11/2026.

## 1. Migrações

```text
$ python manage.py makemigrations tarefas
Migrations for 'tarefas':
  tarefas\migrations\0001_initial.py
    + Create model Categoria
    + Create model Tarefa

$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, tarefas
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying tarefas.0001_initial... OK

$ python manage.py showmigrations tarefas
tarefas
 [X] 0001_initial

$ python manage.py makemigrations --check --dry-run
No changes detected
```

## 2. Dados de teste e Admin

```text
$ python manage.py loaddata dados_iniciais
Installed 5 object(s) from 1 fixture(s)
```

A fixture `tarefas/fixtures/dados_iniciais.json` cria 2 categorias (Estudos, Pessoal) e
3 tarefas (2 pendentes, 1 concluída). Os dados foram carregados pela fixture, e não
digitados no Admin, porque o banco não é versionado e a fixture permite reproduzir o
mesmo estado em qualquer máquina.

Admin respondendo (test client do Django com host `127.0.0.1`, sem login):

```text
302 /admin/login/?next=/admin/
```

## 3. Consultas ORM (`python manage.py shell`)

Executadas por um roteiro que imprime cada comando (`>>>`) e o `repr` do resultado, como
o shell interativo faria:

```text
>>> from tarefas.models import Categoria, Tarefa
>>> Tarefa.objects.all()
<QuerySet [<Tarefa: Revisar models do Django>, <Tarefa: Preparar exercício de Django>, <Tarefa: Organizar documentos pessoais>]>
>>> Tarefa.objects.filter(situacao="PENDENTE")
<QuerySet [<Tarefa: Revisar models do Django>, <Tarefa: Organizar documentos pessoais>]>
>>> Tarefa.objects.order_by("data_prevista")
<QuerySet [<Tarefa: Preparar exercício de Django>, <Tarefa: Revisar models do Django>, <Tarefa: Organizar documentos pessoais>]>
>>> Tarefa.objects.filter(categoria__nome="Estudos")
<QuerySet [<Tarefa: Revisar models do Django>, <Tarefa: Preparar exercício de Django>]>
>>> categoria = Categoria.objects.get(nome="Estudos")
>>> categoria.tarefa_set.all()
<QuerySet [<Tarefa: Revisar models do Django>, <Tarefa: Preparar exercício de Django>]>
```

## 4. Atualização da situação de uma tarefa

```text
>>> tarefa = Tarefa.objects.filter(situacao="PENDENTE").first()
>>> tarefa.pk, tarefa.titulo, tarefa.situacao
(1, 'Revisar models do Django', 'PENDENTE')
>>> tarefa.situacao = "CONCLUIDA"
>>> tarefa.save()
>>> recarregada = Tarefa.objects.get(pk=tarefa.pk)
>>> recarregada.titulo, recarregada.situacao, recarregada.get_situacao_display()
('Revisar models do Django', 'CONCLUIDA', 'Concluída')
>>> Tarefa.objects.filter(situacao="PENDENTE")
<QuerySet [<Tarefa: Organizar documentos pessoais>]>
```

Confirmação em um **novo processo** (outro `manage.py shell`), provando que a alteração
foi gravada no banco e não ficou só na variável Python:

```text
$ python manage.py shell -c "from tarefas.models import Tarefa; print(Tarefa.objects.filter(pk=1).values_list('titulo', 'situacao').get())"
('Revisar models do Django', 'CONCLUIDA')
```

Depois disso o estado inicial foi restaurado com `python manage.py loaddata dados_iniciais`
(`[(1, 'PENDENTE'), (2, 'CONCLUIDA'), (3, 'PENDENTE')]`), para que as evidências seguintes
partam dos dados da fixture.

## 5. Proteção da categoria (`on_delete=PROTECT`)

```text
>>> categoria.delete()
Traceback (most recent call last):
  ...
django.db.models.deletion.ProtectedError: ("Cannot delete some instances of model 'Categoria' because they are referenced through protected foreign keys: 'Tarefa.categoria'.", {<Tarefa: Revisar models do Django>, <Tarefa: Preparar exercício de Django>})
>>> Categoria.objects.count(), Tarefa.objects.count()
(2, 3)
```

O traceback foi encurtado pelo roteiro (`...`); a última linha é a mensagem real da exceção.

## 6. Persistência após reiniciar o servidor

Servidor iniciado com `python manage.py runserver 127.0.0.1:8000 --noreload` em segundo
plano, páginas obtidas com `curl` e tabela extraída do HTML (apenas as linhas da tabela).
Entre o início do servidor 1 e o reinício, a tarefa 1 foi concluída pelo Admin (seção 7).

```text
### Servidor 1
GET /tarefas/ (antes de parar) -> 200
# | Título | Categoria | Data prevista | Prioridade | Situação
2 | Preparar exercício de Django | Estudos | 18/11/2026 | Média | Concluída
1 | Revisar models do Django | Estudos | 21/11/2026 | Alta | Concluída
3 | Organizar documentos pessoais | Pessoal | 25/11/2026 | Baixa | Pendente
Servidor 1 encerrado; porta livre? 000sem resposta (ok)
### Servidor 2
GET /tarefas/ (após reiniciar) -> 200
# | Título | Categoria | Data prevista | Prioridade | Situação
2 | Preparar exercício de Django | Estudos | 18/11/2026 | Média | Concluída
1 | Revisar models do Django | Estudos | 21/11/2026 | Alta | Concluída
3 | Organizar documentos pessoais | Pessoal | 25/11/2026 | Baixa | Pendente
Comparação tabela srv1 x srv2:
idênticas
```

Log do servidor 2 (novo processo):

```text
[20/Nov/2026 08:35:43] "GET /sobre/ HTTP/1.1" 200 72
[20/Nov/2026 08:35:43] "GET /tarefas/ HTTP/1.1" 200 1755
```

Ao final o processo foi encerrado (`nenhum processo escutando na 8000`) e o estado da
fixture foi restaurado com `loaddata dados_iniciais`.

## 7. Registro de validação manual (fluxo principal)

Executado em 20/11/2026 com `curl` contra o servidor local (sem navegador). Para o Admin foi
criado localmente um superusuário descartável (`createsuperuser --noinput`); nenhuma
credencial foi gravada no repositório.

| # | Passo | Esperado | Observado | Evidência |
|---|---|---|---|---|
| 1 | Iniciar o servidor | Responde em 127.0.0.1:8000 | Respondeu | log: `"GET /sobre/ HTTP/1.1" 200 72` |
| 2 | Página inicial `/` | 200 e total vindo do banco | 200, "Existem 3 tarefas cadastradas." | saída abaixo |
| 3 | Lista `/tarefas/` | 3 tarefas, ordem por data, com categoria e data | 200; ordem 18/11, 21/11, 25/11; colunas Categoria e Data prevista | saída abaixo |
| 4 | Pendentes `/tarefas/pendentes/` | Só as tarefas 1 e 3 | 200; tarefas 1 e 3 | saída abaixo |
| 5 | `/sobre/` | 200 com texto | 200, "Sistema de Gestão de Tarefas — ..." | saída abaixo |
| 6 | `/admin/` sem login | Redireciona para o login | `302 /admin/login/?next=/admin/` | saída abaixo |
| 7 | Login no Admin | Sessão autenticada | `302`; páginas do Admin seguintes com 200 (redirecionou para `/accounts/profile/`, ver observação) | saída abaixo |
| 8 | Admin: lista de tarefas | Os 3 registros pelo `__str__` | 200; os 3 títulos | saída abaixo |
| 9 | Admin: editar tarefa 1 e concluir | Salva e volta à lista | GET 200; POST `302 /admin/tarefas/tarefa/` | saída abaixo |
| 10 | Pendentes após concluir | Só a tarefa 3 | 200; só "Organizar documentos pessoais" | saída abaixo |
| 11 | Reiniciar e listar | Mesmos dados | Tabelas idênticas | seção 6 |

```text
GET / -> 200
Existem 3 tarefas cadastradas.
GET /tarefas/ -> 200
# | Título | Categoria | Data prevista | Prioridade | Situação
2 | Preparar exercício de Django | Estudos | 18/11/2026 | Média | Concluída
1 | Revisar models do Django | Estudos | 21/11/2026 | Alta | Pendente
3 | Organizar documentos pessoais | Pessoal | 25/11/2026 | Baixa | Pendente
GET /tarefas/pendentes/ -> 200
# | Título | Categoria | Data prevista | Prioridade | Situação
1 | Revisar models do Django | Estudos | 21/11/2026 | Alta | Pendente
3 | Organizar documentos pessoais | Pessoal | 25/11/2026 | Baixa | Pendente
GET /sobre/ -> Sistema de Gestão de Tarefas — Laboratório de Programação Back End [200]
GET /admin/ (sem login) -> 302 http://127.0.0.1:8000/admin/login/?next=/admin/
POST /admin/login/ -> 302 http://127.0.0.1:8000/accounts/profile/
GET /admin/tarefas/tarefa/ -> 200
  item: Organizar documentos pessoais
  item: Preparar exercício de Django
  item: Revisar models do Django
GET /admin/tarefas/tarefa/1/change/ -> 200
POST edição tarefa 1 (situacao=CONCLUIDA) -> 302 http://127.0.0.1:8000/admin/tarefas/tarefa/
GET /tarefas/pendentes/ (após concluir) -> 200
# | Título | Categoria | Data prevista | Prioridade | Situação
3 | Organizar documentos pessoais | Pessoal | 25/11/2026 | Baixa | Pendente
```

**Observação (não investigada):** no passo 7 o login foi aceito, mas o redirecionamento foi
para `/accounts/profile/`. A requisição foi montada à mão com `curl`; a hipótese é que o
campo `next` não foi enviado como o formulário do navegador envia. Não foi conferido no
navegador. Não afeta o fluxo: a sessão ficou autenticada.

## 8. Falha real registrada

| Item | Registro |
|---|---|
| Fluxo executado | `python manage.py test` logo após trocar a lista `TAREFAS` em memória por consultas ao model (etapa 6) |
| Resultado esperado | Os 3 testes da Semana 6 continuarem passando |
| Resultado observado | `FAILED (failures=1)` em `test_lista_mostra_tarefas`; a página exibiu "Nenhuma tarefa cadastrada." |
| Evidência | Trecho abaixo |
| Causa provável (confirmada) | Os testes dependiam dos dados fixos da lista em memória ("Criar rotas com urls.py"). O Django roda os testes num banco de teste vazio, então a listagem não tinha registros. `test_pendentes_nao_mostra_concluidas` continuou passando só porque a página estava vazia (falso positivo). |
| Validação após correção | `tests.py` reescrito criando categorias e tarefas em `setUpTestData`; `python manage.py test -v 2` → `Ran 13 tests ... OK` (seção 9) |

```text
.F.
======================================================================
FAIL: test_lista_mostra_tarefas (tarefas.tests.RotasTests.test_lista_mostra_tarefas)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\USUARIO\Documents\Gabriel\Lab_BackEnd\primeira_interface_web\tarefas\tests.py", line 12, in test_lista_mostra_tarefas
    self.assertContains(resposta, "Criar rotas com urls.py")
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : Couldn't find 'Criar rotas com urls.py' in the following response
b'<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n [...] <h1>Todas as tarefas</h1>\n\n  \n    <p>Nenhuma tarefa cadastrada.</p>\n  \n\n  <p><a href="/">Voltar ao in\xc3\xadcio</a></p>\n\n</body>\n</html>\n'

----------------------------------------------------------------------
Ran 3 tests in 0.043s

FAILED (failures=1)
```

(Só o meio do HTML da resposta foi cortado, marcado com `[...]`; o resto é a saída real.)

## 9. Testes automatizados

```text
$ python manage.py test -v 2
Found 13 test(s).
test_categoria_com_tarefas_nao_pode_ser_excluida (tarefas.tests.ModelsTests.test_categoria_com_tarefas_nao_pode_ser_excluida) ... ok
test_concluir_tarefa_persiste_no_banco (tarefas.tests.ModelsTests.test_concluir_tarefa_persiste_no_banco) ... ok
test_descricao_pode_ficar_vazia (tarefas.tests.ModelsTests.test_descricao_pode_ficar_vazia) ... ok
test_filtro_por_categoria (tarefas.tests.ModelsTests.test_filtro_por_categoria) ... ok
test_filtro_por_situacao (tarefas.tests.ModelsTests.test_filtro_por_situacao) ... ok
test_str_da_categoria_e_da_tarefa (tarefas.tests.ModelsTests.test_str_da_categoria_e_da_tarefa) ... ok
test_valores_padrao (tarefas.tests.ModelsTests.test_valores_padrao) ... ok
test_inicio_mostra_total_do_banco (tarefas.tests.ViewsTests.test_inicio_mostra_total_do_banco) ... ok
test_lista_mostra_tarefas_com_categoria_e_data (tarefas.tests.ViewsTests.test_lista_mostra_tarefas_com_categoria_e_data) ... ok
test_lista_ordenada_por_data_prevista (tarefas.tests.ViewsTests.test_lista_ordenada_por_data_prevista) ... ok
test_lista_vazia_mostra_mensagem (tarefas.tests.ViewsTests.test_lista_vazia_mostra_mensagem) ... ok
test_pendentes_nao_mostra_concluidas (tarefas.tests.ViewsTests.test_pendentes_nao_mostra_concluidas) ... ok
test_sobre (tarefas.tests.ViewsTests.test_sobre) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.062s

OK
```

(Omitidas as linhas de criação do banco de teste e de `Applying ...`.)

## 10. Revisão técnica

- Nomes: `Categoria`, `Tarefa`, `Prioridade` e `Situacao` em CapWords; funções e variáveis em
  snake_case; indentação de 4 espaços; nenhuma tabulação e nenhuma linha acima de 99 colunas
  nos `.py` (verificado com `grep`/`awk`).
- Código morto: a lista `TAREFAS` e o comentário "EM MEMÓRIA" foram removidos (`grep` sem
  resultados).
- Camadas: model em `models.py`, registro em `admin.py`, consultas nas views, apresentação
  nos templates.
- Segredos: `git grep -nEi "password|secret|token" -- primeira_interface_web` retornou:

  ```text
  primeira_interface_web/gestao_tarefas/settings.py:7:SECRET_KEY = "django-insecure-troque-esta-chave-em-producao"
  primeira_interface_web/gestao_tarefas/settings.py:57:AUTH_PASSWORD_VALIDATORS = []
  ```

  A `SECRET_KEY` é a chave de laboratório existente desde a Semana 6, marcada como
  `django-insecure` e comentada como "apenas para desenvolvimento"; não protege dados reais.
  `AUTH_PASSWORD_VALIDATORS` é configuração, não credencial. `db.sqlite3` e `.venv` estão no
  `.gitignore`.

## 11. Checklist de conclusão (enunciado da Semana 07)

- [x] A aplicação está registrada nas configurações do projeto. (`"tarefas"` em `INSTALLED_APPS`, `gestao_tarefas/settings.py`)
- [x] O model Categoria possui um campo de nome. (`tarefas/models.py`)
- [x] O model Tarefa possui título, descrição, prioridade, data prevista, situação e categoria. (`tarefas/models.py`)
- [x] O relacionamento usa ForeignKey para Categoria. (`on_delete=PROTECT`; seção 5)
- [x] As migrações foram criadas e aplicadas. (seção 1; `0001_initial.py` versionado)
- [x] Os dois models foram registrados no Django Admin. (`tarefas/admin.py`; seção 7, passos 8–9)
- [x] Há categorias e tarefas cadastradas. (fixture, seção 2)
- [x] Uma consulta filtrada pelo ORM foi executada. (seção 3)
- [x] A situação de uma tarefa foi atualizada e salva. (seção 4 pelo shell; seção 7 pelo Admin)
- [x] Os dados continuaram disponíveis após reiniciar o servidor. (seção 6)
- [x] A evolução foi registrada em um commit descritivo. (`git log` da branch `semana-07-persistencia`)

## 12. Checklist final de entrega (Semana 10)

- [x] O ambiente virtual e as dependências estão documentados. (`README.md` desta pasta)
- [x] As migrações necessárias estão presentes e podem ser aplicadas. (seção 1 e teste de reprodutibilidade em pasta limpa)
- [x] A aplicação inicia sem erro seguindo o README. (seção 6 e teste de reprodutibilidade)
- [x] Os fluxos principais foram testados e possuem evidências. (seções 7 e 9; criar/editar/excluir pelas páginas não existe nesta versão, só pelo Admin)
- [x] Ao menos uma falha encontrada foi registrada e validada após a correção. (seção 8)
- [x] O código possui nomes compreensíveis e organização coerente. (seção 10)
- [x] Não há credenciais, chaves ou dados sensíveis no repositório. (seção 10; só a `SECRET_KEY` de laboratório)
- [x] O README apresenta instalação, execução, uso, funcionalidades e limitações. (`README.md`)
- [ ] A equipe consegue explicar uma decisão técnica e uma melhoria futura. (Depende da apresentação do aluno; o README traz material de apoio, como o uso de `PROTECT` e a paginação como melhoria futura, mas isso só se comprova na demonstração.)
