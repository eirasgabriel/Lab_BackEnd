# 08 · Registro de entrega (preenchido)

Preenche o "Registro de entrega" e a "Definição de pronto" de [06_ENTREGA.md](06_ENTREGA.md).
As saídas abaixo foram copiadas dos comandos executados; nenhuma foi editada além de
cortes indicados.

## Registro de entrega

- **Versão:** projeto SIGA importado sem alterações de código no repositório `Lab_BackEnd`,
  pasta `siga_django/`, branch `siga-django` (commit de importação `2ac5329`).
- **Data:** 20/11/2026
- **Integrantes:** ____
- **Python/Django:** Python 3.14.10 (Windows 10, instalado via `uv`), Django 6.0.5, SQLite.
  O ambiente virtual fica em `siga_django/.venv`, separado do `.venv` da raiz (que usa
  Django 5.2 para `primeira_interface_web/`).

### Comandos executados e resultados

```text
$ python manage.py check
System check identified no issues (0 silenced).
$ python manage.py makemigrations --check --dry-run
No changes detected
(código de saída: 0)
$ python manage.py migrate
Operations to perform:
  Apply all migrations: academico, admin, auth, contenttypes, sessions
Running migrations:
  Applying academico.0001_initial... OK
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
$ python manage.py dados_demo
Dados demonstrativos disponíveis.
$ python manage.py dados_demo   (2ª vez, idempotência)
Dados demonstrativos disponíveis.
```

Depois das duas execuções de `dados_demo`, o banco tinha `alunos 3 turmas 1 matriculas 3`
(sem duplicação).

```text
$ python manage.py test -v 2
Found 16 test(s).
test_banco_rejeita_matricula_duplicada (academico.tests.SistemaTests.test_banco_rejeita_matricula_duplicada) ... ok
test_banco_rejeita_nota_invalida (academico.tests.SistemaTests.test_banco_rejeita_nota_invalida) ... ok
test_cadastros_relacionados (academico.tests.SistemaTests.test_cadastros_relacionados) ... ok
test_crud_aluno (academico.tests.SistemaTests.test_crud_aluno) ... ok
test_csrf_obrigatorio (academico.tests.SistemaTests.test_csrf_obrigatorio) ... ok
test_demo_idempotente (academico.tests.SistemaTests.test_demo_idempotente) ... ok
test_fluxo_matricula_e_boletim (academico.tests.SistemaTests.test_fluxo_matricula_e_boletim) ... ok
test_formulario_invalido_nao_persiste (academico.tests.SistemaTests.test_formulario_invalido_nao_persiste) ... ok
test_leitor_consulta_mas_nao_altera (academico.tests.SistemaTests.test_leitor_consulta_mas_nao_altera) ... ok
test_login_e_logout (academico.tests.SistemaTests.test_login_e_logout) ... ok
test_matricula_aluno_unica (academico.tests.SistemaTests.test_matricula_aluno_unica) ... ok
test_notas_invalidas (academico.tests.SistemaTests.test_notas_invalidas) ... ok
test_notas_limites_e_pendencia (academico.tests.SistemaTests.test_notas_limites_e_pendencia) ... ok
test_protecao_de_relacionamentos (academico.tests.SistemaTests.test_protecao_de_relacionamentos) ... ok
test_rotas_inexistentes (academico.tests.SistemaTests.test_rotas_inexistentes) ... ok
test_visitante_precisa_login (academico.tests.SistemaTests.test_visitante_precisa_login) ... ok

----------------------------------------------------------------------
Ran 16 tests in 4.186s

OK
```

(Omitidas as linhas de criação do banco de teste e de `Applying ...`.)

**Reprodutibilidade:** o conteúdo commitado de `siga_django/` foi extraído (`git archive`)
para uma pasta temporária vazia e o README foi seguido: venv → `pip install -r
requirements.txt` → `migrate` → `dados_demo` → `test`. Resultado: `Applying
sessions.0001_initial... OK`, `Dados demonstrativos disponíveis.`, `Ran 16 tests in
3.937s` / `OK`. O passo `createsuperuser` do README é interativo e não foi repetido nessa
pasta. Como não há `python` no PATH desta máquina, o venv foi criado chamando o executável
do Python 3.14 pelo caminho completo.

### Testes exploratórios executados

Roteiro de [03_TESTES.md](03_TESTES.md), executado em 20/11/2026 por requisições HTTP reais
(script Python com `urllib`, cookies de sessão e token CSRF) contra
`python manage.py runserver 127.0.0.1:8000 --noreload`. **Não foi usado navegador.** Foram
criados localmente duas contas descartáveis: uma superusuária (editor, via
`createsuperuser --noinput`) e uma comum sem `is_staff` (leitor). As senhas foram geradas
aleatoriamente, mantidas só em variáveis de ambiente da sessão e não foram gravadas.

| # | Ação | Resultado esperado | Observado | Situação |
|---|---|---|---|---|
| 1 | Entrar com senha errada | Mensagem de erro sem autenticar | `POST /entrar/` → 200 com "Por favor, entre com um usuário e senha corretos. ..."; `GET /` depois → `302 /entrar/?next=/` | Conforme |
| 2 | Cadastrar professor, disciplina, turma e aluno | Registros disponíveis nos seletores | 4 POSTs → 302 para as listas; seletor aluno inclui "Aluno Exploratorio (EXP100)"; seletor turma inclui "EXP-T1 - Teste Exploratorio" | Conforme |
| 3 | Matricular com notas vazias | Situação Pendente | Linha: `— — — Pendente` | Conforme |
| 4 | Notas 5 e 7 | Média 6 e Aprovado | Linha: `5,00 7,00 6,00 Aprovado` | Conforme |
| 5 | Notas 0 e 0 | Média 0 e Reprovado | Linha: `0,00 0,00 0,00 Reprovado` | Conforme |
| 6 | Nota 11 ou matrícula duplicada | Erro no formulário; nada inválido salvo | Nota 11: 200 com "Certifique-se que este valor seja menor ou igual a 10." e linha inalterada (`0,00 0,00`); duplicada: 200 com "Matricula com este Aluno e Turma já existe." e 1 matrícula do aluno na lista | Conforme |
| 7 | Excluir disciplina ou professor vinculado à turma | Mensagem sobre registros vinculados | Ambos: 302 + "Não é possível excluir: existem registros vinculados."; continuam listados | Conforme |
| 8 | Abrir confirmação e cancelar | Nenhum dado removido | `GET /alunos/4/excluir/` → 200 ("Confirmar exclusão ... Cancelar"); link Cancelar → `/alunos/` 200; aluno continua listado | Conforme (o clique foi simulado seguindo o link) |
| 9 | Excluir matrícula e depois aluno sem vínculos | Exclusões permitidas | Ambos: 302 + "Registro excluído."; aluno não aparece mais | Conforme |
| 10 | Leitor tenta URL de edição | Escrita recusada por redirecionamento | Lista 200 sem "Novo registro"; `GET` e `POST /turmas/2/editar/` → `302 /entrar/?next=/turmas/2/editar/`; turma não foi alterada | Conforme |
| 11 | Sair e atualizar página protegida | Solicitação de login | `POST /sair/` → `302 /entrar/`; `GET /matriculas/` → `302 /entrar/?next=/matriculas/` | Conforme |
| 12 | Fechar e reiniciar o servidor | Dados persistem no SQLite | Após parar (porta sem resposta, código `000`) e subir de novo: professor, disciplina e turma criados continuam; aluno excluído continua ausente; dados demo presentes; painel "3 alunos 2 turmas 3 matrículas" | Conforme |

**Conferência no navegador (20/11/2026):** depois do roteiro por HTTP, o fluxo foi repetido
no navegador com um superusuário e um leitor sem "Membro da equipe", criados localmente
(sem senhas registradas). Log do servidor nesse trecho:

```text
[20/Nov/2026 09:14:48] "GET /turmas/1/editar/ HTTP/1.1" 302 0
[20/Nov/2026 09:14:48] "GET /entrar/?next=/turmas/1/editar/ HTTP/1.1" 200 1585
[20/Nov/2026 09:15:42] "POST /sair/ HTTP/1.1" 302 0
[20/Nov/2026 09:15:44] "GET /matriculas/ HTTP/1.1" 302 0
[20/Nov/2026 09:15:44] "GET /entrar/?next=/matriculas/ HTTP/1.1" 200 1154
[20/Nov/2026 09:16:08] "POST /entrar/ HTTP/1.1" 302 0
[20/Nov/2026 09:16:26] "GET /matriculas/5/editar/ HTTP/1.1" 200 2154
[20/Nov/2026 09:16:32] "POST /matriculas/5/editar/ HTTP/1.1" 200 2319
[20/Nov/2026 09:16:42] "GET /disciplinas/3/excluir/ HTTP/1.1" 200 1147
[20/Nov/2026 09:16:43] "POST /disciplinas/3/excluir/ HTTP/1.1" 302 0
[20/Nov/2026 09:16:43] "GET /disciplinas/ HTTP/1.1" 200 1606
```

| Verificação no navegador | Observado |
|---|---|
| Leitor consulta as listas | Alunos, professores, turmas e matrículas abriram (200) |
| Leitor abre URL de edição | `302 /entrar/?next=/turmas/1/editar/` |
| Sair e recarregar página protegida | `POST /sair/` e depois `GET /matriculas/` → `302 /entrar/?next=/matriculas/` |
| Editor: nota 11 na tela do SIGA | `POST /matriculas/5/editar/` → 200 (formulário com erro); notas continuaram 5,00 e 7,00 no banco |
| Editor: excluir disciplina vinculada | `POST /disciplinas/3/excluir/` → 302; disciplina continuou no banco (3 disciplinas) |
| Notas 5 e 7 | Média 6,00 e Aprovado |

Nessa conferência, professor, disciplina, turma, aluno e a matrícula com notas 5 e 7 foram
cadastrados pelo Django Admin, e não pelos formulários do SIGA. A criação pelos formulários
do SIGA foi verificada só no roteiro HTTP (ações 2 a 5). A aparência das páginas (CSS,
layout) não foi avaliada formalmente.

Saída do roteiro (convertida de cp1252 para UTF-8; conteúdo inalterado):

```text
## Ação 1: Entrar com senha errada
   POST /entrar/ -> 200
   erros: ['Por favor, entre com um usuário e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.']
   GET / em seguida -> 302 /entrar/?next=/

## Ação 2: Cadastrar professor, disciplina, turma e aluno
   login editor -> 302 /
   POST /professores/novo/ -> 302 /professores/
   POST /disciplinas/novo/ -> 302 /disciplinas/
   POST /turmas/novo/ -> 302 /turmas/
   POST /alunos/novo/ -> 302 /alunos/
   seletor aluno: ['---------', 'Aluno Exploratorio (EXP100)', 'Ana Exemplo (DEMO1)', 'Bruno Exemplo (DEMO2)', 'Carla Exemplo (DEMO3)']
   seletor turma: ['---------', 'BE-2026-2 - Laboratório Back End', 'EXP-T1 - Teste Exploratorio']

## Ação 3: Matricular aluno com notas vazias
   POST /matriculas/novo/ -> 302 /matriculas/
   linha: ['Aluno Exploratorio / EXP-T1 — — — Pendente Editar · Excluir']

## Ação 4: Informar notas 5 e 7
   POST editar -> 302 /matriculas/
   linha: ['Aluno Exploratorio / EXP-T1 5,00 7,00 6,00 Aprovado Editar · Excluir']

## Ação 5: Informar notas 0 e 0
   POST editar -> 302 /matriculas/
   linha: ['Aluno Exploratorio / EXP-T1 0,00 0,00 0,00 Reprovado Editar · Excluir']

## Ação 6: Tentar nota 11 ou matrícula duplicada
   nota 11: POST editar -> 200 (sem redirect)
   erros: ['Certifique-se que este valor seja menor ou igual a 10.']
   linha após tentativa: ['Aluno Exploratorio / EXP-T1 0,00 0,00 0,00 Reprovado Editar · Excluir']
   duplicada: POST /matriculas/novo/ -> 200 (sem redirect)
   erros: ['Matricula com este Aluno e Turma já existe.']
   matrículas do aluno na lista: 1

## Ação 7: Excluir disciplina ou professor vinculado à turma
   POST /disciplinas/2/excluir/ -> 302 /disciplinas/
   aviso: ['Não é possível excluir: existem registros vinculados.']
   ainda listado: True
   POST /professores/2/excluir/ -> 302 /professores/
   aviso: ['Não é possível excluir: existem registros vinculados.']
   ainda listado: True

## Ação 8: Abrir confirmação de exclusão e cancelar
   GET /alunos/4/excluir/ -> 200; texto: Confirmar exclusão Aluno Exploratorio (EXP100) Confirmar exclusão Cancelar
   link Cancelar -> /alunos/; GET -> 200
   aluno ainda listado: True

## Ação 9: Excluir matrícula e depois aluno sem outros vínculos
   POST /matriculas/4/excluir/ -> 302 /matriculas/; aviso: ['Registro excluído.']
   POST /alunos/4/excluir/ -> 302 /alunos/; aviso: ['Registro excluído.']
   aluno ainda listado: False

## Ação 10: Entrar como leitor e tentar URL de edição
   login leitor -> 302 /
   GET /turmas/ -> 200; link 'Novo registro' visível: False
   GET /turmas/2/editar/ -> 302 /entrar/?next=/turmas/2/editar/
   POST /turmas/2/editar/ -> 302 /entrar/?next=/turmas/2/editar/
   turma renomeada para INVADIDO: False

## Ação 11: Sair e atualizar página protegida
   POST /sair/ -> 302 /entrar/
   GET /matriculas/ -> 302 /entrar/?next=/matriculas/

(fim da fase 1)
servidor 1 parado; resposta agora: 000

## Ação 12: Fechar e reiniciar servidor (após reinício)
   login editor -> 302 /
   /professores/ contém 'Prof Exploratorio': True
   /disciplinas/ contém 'EXP01': True
   /turmas/ contém 'EXP-T1': True
   /alunos/ contém 'EXP100': False
   /alunos/ contém 'DEMO1': True
   painel: PROJETO INTEGRADOR Integração e entrega Cadastros, matrículas e resultados em um único sistema. 3 alunos 2 turmas 3 matrículas Como começar Cadastre professor e
```

(O texto do painel foi cortado em 160 caracteres pelo próprio script.)

### Requisitos não atendidos ou limitações

- Escopo declarado em [01_REQUISITOS.md](01_REQUISITOS.md): sem paginação, frequência,
  recuperação de senha, gestão financeira ou isolamento por docente; semestre é texto livre.
- Configuração de desenvolvimento: `SECRET_KEY` fixa de laboratório
  (`'somente-laboratorio-nao-utilizar-em-producao'`), `DEBUG = True`, `runserver`. Não serve
  para publicação (ver "Publicação futura" em 06_ENTREGA.md).
- **CI não roda nesta posição:** o GitHub só executa workflows em `.github/workflows/` na raiz
  do repositório. O arquivo foi mantido em `siga_django/.github/workflows/testes.yml`, sem
  mover; para ativá-lo seria preciso movê-lo para a raiz e ajustar `working-directory:
  siga_django`. A execução remota não foi verificada.
- O projeto exige Django 6.0.5 (Python 3.12 a 3.14), incompatível com o Django 5.2 de
  `primeira_interface_web/`; por isso usa um `.venv` próprio dentro de `siga_django/`.
- A aparência das páginas (CSS, layout) não foi avaliada formalmente.

### Refatoração e evidência antes/depois

Não realizada nesta entrega. O exercício de [04_REFATORACAO.md](04_REFATORACAO.md)
corresponde a uma questão da Arguição Prática, que é presencial e individual; fica para o
aluno fazer em aula.

### Próximas ações e responsáveis

____

## Definição de pronto

- [x] Requisitos implementados e limitações declaradas. (R01–R12 cobertos pela suíte de 16 testes; R09 para professor/disciplina conferido na ação 7; limitações na seção acima)
- [x] check sem erros; migrações sem pendências; suíte aprovada. (saídas acima)
- [x] Fluxo manual com editor e leitor conferido no navegador. (Seção "Conferência no navegador": autorização do leitor, logout, nota inválida e proteção de vínculo pelas telas do SIGA. Os cadastros dessa conferência foram feitos pelo Admin; a criação pelos formulários do SIGA está no roteiro HTTP, ações 2–5.)
- [ ] README seguido em uma pasta nova por outro integrante. (Foi seguido em pasta nova, mas pelo mesmo ambiente, não por outro integrante.)
- [x] Migrações e requirements incluídos; banco e ambiente virtual excluídos. (`git ls-files` lista `academico/migrations/0001_initial.py` e `requirements.txt`; nenhum `.venv` ou `db.sqlite3`)
- [ ] Documentação, evidências e retrospectiva atualizadas. (Documentação e evidências: este arquivo. A retrospectiva de [05_AULA_DEMONSTRACAO.md](05_AULA_DEMONSTRACAO.md) é da turma e não foi feita.)
- [ ] ZIP abre na IDE e contém manage.py na pasta principal do projeto. (Não se aplica: a entrega aqui é pelo repositório Git; `manage.py` está em `siga_django/`. Nenhum ZIP foi gerado.)
