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
