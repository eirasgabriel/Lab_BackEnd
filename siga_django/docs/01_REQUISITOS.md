# 01 · Requisitos e aceitação

Problema: uma secretaria precisa organizar cadastros e notas sem planilhas isoladas.
Entrega: um sistema local em que o operador segue o fluxo até consultar o resultado.
A média mínima 6 é uma decisão didática, não uma regra da universidade.

| ID | Requisito | Critério verificável | Evidência automatizada em SistemaTests |
| --- | --- | --- | --- |
| R01 | Autenticar | Visitante é redirecionado; login permite entrar; logout encerra sessão | test_visitante_precisa_login; test_login_e_logout |
| R02 | Autorizar | Leitor consulta, mas não salva nem exclui | test_leitor_consulta_mas_nao_altera |
| R03 | CRUD de alunos | Criar, listar, editar e excluir sem vínculos; GET não exclui | test_crud_aluno |
| R04 | Validar aluno | Nome e e-mail válidos; matrícula única | test_formulario_invalido_nao_persiste; test_matricula_aluno_unica |
| R05 | Organizar oferta | Cadastrar professor, disciplina e turma relacionada | test_cadastros_relacionados |
| R06 | Matricular | Um aluno não pode se matricular duas vezes na mesma turma | test_fluxo_matricula_e_boletim; test_banco_rejeita_matricula_duplicada |
| R07 | Validar notas | Cada nota é opcional; quando preenchida, deve estar entre 0 e 10 | test_notas_invalidas; test_banco_rejeita_nota_invalida |
| R08 | Calcular resultado | Duas notas: média aritmética; média ≥ 6 aprova; nota ausente deixa pendente | test_notas_limites_e_pendencia |
| R09 | Proteger histórico | Aluno, professor, disciplina ou turma com vínculos não podem ser excluídos | test_protecao_de_relacionamentos (aluno); demais vínculos: roteiro manual |
| R10 | Consultar | Pesquisa parcial pelo nome do aluno | test_crud_aluno |
| R11 | Entregar repetivelmente | Comando de demonstração não duplica registros | test_demo_idempotente |
| R12 | Proteger POST | Requisições sem token CSRF são recusadas | test_csrf_obrigatorio |

Requisitos de qualidade: código separado por responsabilidade; dependência fixada;
migração versionada; testes sem alterar dados de aula; instruções reproduzíveis.
Sem paginação, frequência, recuperação, gestão financeira ou isolamento por docente.
Campo semestre é texto livre nesta versão. Não há promessa de cobertura de 100%.
