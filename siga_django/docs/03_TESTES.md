# 03 · Testes, diagnóstico e evidências

Execute os comandos usando o Python do ambiente virtual indicado no README:

```text
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test -v 2
python manage.py test academico.tests.SistemaTests.test_fluxo_matricula_e_boletim -v 2
```

check inspeciona a configuração; não comprova comportamento. O segundo comando
detecta alterações em Models sem migrações. test cria um banco temporário, executa
os casos e o descarta. Não use o banco real como base de testes.

Um teste segue três partes: preparação (dados conhecidos), ação (requisição ou
chamada) e verificação (assert). setUpTestData cria dados para a classe;
setUp autentica o cliente antes de cada teste. O cliente do Django simula HTTP
sem abrir um navegador. force_login isola os testes das funcionalidades do login;
test_login_e_logout exercita o login separadamente.

Testes de regra verificam media/situacao. Testes de formulário verificam entradas
inválidas. Testes integrados percorrem URL, view, form, ORM e template.
test_csrf_obrigatorio usa enforce_csrf_checks porque o cliente de teste normalmente
desabilita essa checagem. Isso não substitui um teste completo em navegador.

## Roteiro exploratório no navegador

| Ação | Resultado esperado |
| --- | --- |
| Entrar com senha errada | Mensagem de erro sem autenticar |
| Cadastrar professor, disciplina, turma e aluno | Registros disponíveis nos seletores |
| Matricular aluno e deixar as notas vazias | Situação Pendente |
| Informar notas 5 e 7 | Média 6 e situação Aprovado |
| Informar notas 0 e 0 | Média 0 e situação Reprovado |
| Tentar nota 11 ou matrícula duplicada | Erro no formulário; nada inválido salvo |
| Excluir disciplina ou professor vinculado à turma | Mensagem sobre registros vinculados |
| Abrir confirmação de exclusão e cancelar | Nenhum dado removido |
| Excluir matrícula e depois aluno sem outros vínculos | Exclusões permitidas |
| Entrar como leitor e tentar URL de edição | Escrita recusada por redirecionamento |
| Sair e atualizar página protegida | Solicitação de login |
| Fechar e reiniciar servidor | Dados persistem no SQLite |

Registre: data, versão, ambiente, requisito, entrada, esperado, observado e responsável.
Se um teste falhar, leia a última exceção, localize o arquivo e reproduza apenas
aquele caso; corrija e depois execute a suíte inteira. Não altere a expectativa
só para obter verde: confirme primeiro a regra acordada.

## Diagnóstico rápido

- No module named django: confira o executável e instale requirements.txt.
- no such table: execute migrate no mesmo diretório e ambiente.
- Erro 403: confira csrf_token e cookies; não remova o middleware como solução.
- Editor não acessa /admin/: conceda permissões de modelos ou use o superusuário.
- Nota não aparece como média: confirme se ambas as notas foram preenchidas.
