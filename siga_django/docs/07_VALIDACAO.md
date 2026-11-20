# 07 · Validação desta entrega

Ambiente verificado: Python 3.14.3, Django 6.0.5 e SQLite, Windows.

- `python manage.py check`: nenhum problema identificado.
- `python manage.py makemigrations --check --dry-run`: nenhuma alteração pendente.
- `python manage.py test -v 2`: 16 testes aprovados.
- A migração inicial foi aplicada com sucesso ao banco temporário dos testes.

Os testes verificam regras de notas, validação, CRUD de alunos, criação dos cadastros
relacionados, matrícula, autenticação, autorização, CSRF, proteção de vínculos,
restrições de banco e dados demonstrativos idempotentes.

As respostas HTML foram exercitadas pelo cliente de testes do Django. A revisão visual
em navegador e a execução do workflow no GitHub não foram realizadas neste ambiente.
O roteiro exploratório está em 03_TESTES.md para orientar essas verificações em aula.
