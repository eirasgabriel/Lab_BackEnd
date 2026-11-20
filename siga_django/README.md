# SIGA — Integração e entrega com Django

Laboratório de Programação Back End · Engenharia de Software · 2026.2
Prof. Ralfh Varges Ansuattigui

Aplicação didática completa para execução local: alunos, professores, disciplinas,
turmas, matrículas, lançamento de duas notas, média, situação e pesquisa de alunos.
Login obrigatório; leitores consultam e membros da equipe alteram.
HTML renderizado no servidor, CSS local e SQLite: sem Node, API externa ou CDN.

## Executar no Windows / VS Code

Descompacte a pasta e abra-a no VS Code. No terminal, na pasta que contém manage.py:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py dados_demo
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver
```

Abra http://127.0.0.1:8000/ e entre com a conta que você criou.
O uso direto do executável evita problemas com a política de ativação do PowerShell.
O download inicial das dependências exige internet. Python 3.12 a 3.14;
a versão fixada do Django é 6.0.5, utilizada na validação desta entrega.
Em Linux/macOS, substitua `.\.venv\Scripts\python.exe` por `.venv/bin/python`.

## Contas e administração

Acesse /admin/ com o superusuário. Em Usuários, crie uma conta comum para leitura
(sem “Membro da equipe”) e outra com “Membro da equipe” para edição.
Para entrar no painel administrativo, o editor também precisa das permissões
específicas dos modelos; as telas didáticas usam apenas o indicador is_staff.
Não há senhas prontas nem cadastro público. Todos os leitores veem todos os dados:
os usuários representam operadores acadêmicos, não portais individuais de alunos.

## Ordem de leitura

1. [Requisitos e critérios de aceitação](docs/01_REQUISITOS.md)
2. [Guia de análise do código](docs/02_GUIA_ALUNO.md)
3. [Testes e diagnóstico](docs/03_TESTES.md)
4. [Refatoração guiada](docs/04_REFATORACAO.md)
5. [Demonstração e retrospectiva](docs/05_AULA_DEMONSTRACAO.md)
6. [Checklist de integração e entrega](docs/06_ENTREGA.md)

## Organização

| Caminho | Responsabilidade |
| --- | --- |
| manage.py | Entrada dos comandos Django |
| config/ | Configuração, rotas principais e WSGI |
| academico/models.py | Entidades, relações, média e situação |
| academico/forms.py | Entrada e validação de dados |
| academico/views.py | Tratamento das requisições HTTP |
| academico/urls.py | Rotas da aplicação |
| academico/tests.py | Testes com banco temporário |
| academico/migrations/ | Histórico do esquema do banco |
| templates/ | Páginas e reutilização de layout |
| static/ | Folha de estilo local |
| docs/ | Guias, critérios e roteiros de entrega |

Banco de demonstração é criado por migrate + dados_demo; o ZIP não inclui banco,
usuários reais ou ambiente virtual. Interrompa o servidor com Ctrl+C.
Se a porta estiver ocupada, use `manage.py runserver 8001`.

## Base pedagógica e referências

Planejamento de Ensino — Laboratório de Programação Back End, Univassouras,
Campus Saquarema, 2026.2, de 19/08/2026: Prática 2, Sistema Integrado de Gestão
Acadêmica; objetivos de CRUD, autenticação, validação, testes e documentação.
Aula 01 — Apresentação Atualizada: encontro 10, Integração e entrega.
Este material concretiza esse escopo em um exemplo pequeno e funcional.

Documentação oficial:
- https://docs.djangoproject.com/en/6.0/intro/tutorial01/
- https://docs.djangoproject.com/en/6.0/topics/forms/modelforms/
- https://docs.djangoproject.com/en/6.0/topics/testing/overview/
- https://docs.djangoproject.com/en/6.0/topics/auth/default/
- https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
