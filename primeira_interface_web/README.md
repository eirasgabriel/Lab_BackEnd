# Sistema Web de Gestão de Tarefas (Django)

## 1. Objetivo
Aplicação web para organizar tarefas por categoria, prioridade, data prevista e situação
(pendente ou concluída). Começou na Semana 6 com dados em memória; na Semana 7 passou a
guardar categorias e tarefas no banco de dados, de modo que os registros continuam
disponíveis depois que o servidor é reiniciado.

## 2. Tecnologias
- Python
- Django 5.2 (`requirements.txt`: `Django>=5.0,<6.0`)
- SQLite (arquivo local `db.sqlite3`, criado pelo `migrate` e não versionado)

## 3. Pré-requisitos
- Python 3.10 ou superior (exigência do Django 5.x). Versão usada no desenvolvimento e na
  validação: **Python 3.15.2**, com Django 5.2.19.
- Git e um terminal.

## 4. Ambiente virtual
O ambiente virtual fica na **raiz do repositório** (`Lab_BackEnd/.venv`), como descrito no
README principal:

```bash
# na raiz do repositório
python -m venv .venv
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # Linux/macOS
```

## 5. Instalação das dependências
```bash
pip install -r primeira_interface_web/requirements.txt
```

## 6. Banco de dados (migrações e dados de exemplo)
Todos os comandos `manage.py` são executados dentro de `primeira_interface_web/`:

```bash
cd primeira_interface_web
python manage.py migrate                    # cria db.sqlite3 e as tabelas
python manage.py loaddata dados_iniciais    # 2 categorias e 3 tarefas de exemplo
```

A fixture `tarefas/fixtures/dados_iniciais.json` cria as categorias "Estudos" e "Pessoal"
e três tarefas (duas pendentes e uma concluída). Rodar `loaddata` de novo restaura esses
registros ao estado original.

## 7. Execução
```bash
python manage.py runserver
```
Abra http://127.0.0.1:8000/

## 8. Uso
- **Páginas públicas:** consultar todas as tarefas ou só as pendentes (somente leitura).
- **Django Admin** (http://127.0.0.1:8000/admin/): cadastrar, editar e excluir categorias e
  tarefas. Crie uma conta administrativa antes:
  ```bash
  python manage.py createsuperuser
  ```
- **ORM pelo shell:**
  ```bash
  python manage.py shell
  ```
  ```python
  from tarefas.models import Categoria, Tarefa
  Tarefa.objects.filter(situacao="PENDENTE")
  Tarefa.objects.filter(categoria__nome="Estudos")
  Tarefa.objects.order_by("data_prevista")
  ```

## 9. Funcionalidades implementadas
- Models `Categoria` (nome) e `Tarefa` (título, descrição opcional, prioridade, data
  prevista, situação e categoria), com migração versionada em `tarefas/migrations/`.
- Uma categoria com tarefas não pode ser excluída (`on_delete=PROTECT`).
- Models registrados no Django Admin.
- Rotas:

| URL | View | Resposta |
|---|---|---|
| `/` | `inicio` | `inicio.html` com o total de tarefas do banco |
| `/tarefas/` | `lista_tarefas` | `lista.html` com todas as tarefas, ordenadas por data prevista |
| `/tarefas/pendentes/` | `tarefas_pendentes` | `lista.html` só com as pendentes |
| `/sobre/` | `sobre` | `HttpResponse` (texto) |
| `/admin/` | Django Admin | administração de categorias e tarefas |

A listagem mostra título, categoria, data prevista (dd/mm/aaaa), prioridade e situação.

Fluxo: Navegador → `gestao_tarefas/urls.py` → `tarefas/urls.py` → `views.py` → ORM
(`models.py`) → template → resposta.

## 10. Limitações conhecidas
- Não há formulários nas páginas públicas: criar, editar, concluir e excluir só pelo Admin
  ou pelo shell.
- Não há autenticação nas páginas públicas; qualquer pessoa com acesso ao servidor vê as
  tarefas.
- Não há filtro por categoria nem paginação na listagem.
- `SECRET_KEY` fixa e `DEBUG = True` são configurações de laboratório; não servem para
  produção.
- O banco `db.sqlite3` é local e não vai para o repositório: cada pessoa recria os dados
  com `migrate` + `loaddata`.

## Testes
```bash
python manage.py test
```
São 13 testes (`tarefas/tests.py`): `__str__`, valores padrão, descrição vazia, conclusão
persistida, proteção da categoria, filtros por situação e por categoria, e as views
(início, lista ordenada com categoria e data, pendentes, lista vazia e sobre). Os testes
criam seus próprios dados em um banco de teste e não dependem do `db.sqlite3` local.

Evidências de execução (migrações, consultas ORM, reinício do servidor, validação manual e
checklists): [EVIDENCIAS_SEMANA_07.md](EVIDENCIAS_SEMANA_07.md).

## Dificuldade encontrada e como foi resolvida
Ao trocar a lista `TAREFAS` em memória por consultas ao model, o teste
`test_lista_mostra_tarefas` da Semana 6 falhou (`FAILED (failures=1)`): ele procurava a
tarefa "Criar rotas com urls.py", que existia só na lista fixa. O Django executa os testes
num banco de teste vazio, então a página mostrava "Nenhuma tarefa cadastrada.". Percebemos
também que o teste das pendentes passava apenas porque a página estava vazia. A solução foi
reescrever os testes para criar categorias e tarefas no próprio teste (`setUpTestData`) e
verificar o conteúdo real da página; depois disso, os 13 testes passaram. O registro
completo está na seção 8 de [EVIDENCIAS_SEMANA_07.md](EVIDENCIAS_SEMANA_07.md).
