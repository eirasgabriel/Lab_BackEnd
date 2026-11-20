# 02 · Guia de análise e entendimento

## 1. Primeiro execute e observe

Siga o README. Carregue dados_demo, entre e abra cada cadastro. Antes de ler o código,
descreva como um professor, uma disciplina e uma turma se relacionam.
Não comece alterando todos os arquivos: observe um fluxo completo.

## 2. Caminho de uma requisição

Ao abrir `/alunos/`, config/urls.py delega a academico/urls.py. A rota entrega
entidade='alunos' à função listar. O decorador login_required verifica a sessão.
configuracao consulta o dicionário CADASTROS; o ORM consulta Aluno;
render combina lista.html com os dados. O navegador recebe HTML, não objetos Python.

Ao salvar, o navegador envia POST. salvar cria AlunoForm com request.POST;
is_valid verifica tipos, campos e unicidade. Se inválido, a mesma tela mostra erros.
Se válido, form.save grava via ORM e redirect provoca um novo GET da listagem.
Esse redirecionamento evita repetir o POST ao atualizar a tela.

Exercício: acompanhe esses passos no depurador do VS Code com pontos de parada
em salvar, em form.is_valid e em form.save. Inspecione request.method,
request.POST, form.errors e objeto. Nunca registre senhas em logs.

## 3. Leia o Model antes da View

`class Aluno(models.Model)` usa herança: Django fornece persistência.
`CharField` define texto limitado; `unique=True` exige unicidade.
`ForeignKey` é uma relação muitos-para-um: uma turma tem uma disciplina;
várias turmas podem compartilhar a mesma disciplina.
`on_delete=PROTECT` impede apagar um registro referenciado.

Matricula liga aluno e turma. UniqueConstraint protege esse par.
Validadores informam erros amigáveis no formulário; CheckConstraint também protege
a integridade quando alguém usa o ORM diretamente. save() não chama full_clean().
Para scripts com mensagens de validação, chame full_clean() antes de save().

`@property` deixa media e situacao acessíveis como atributos sem armazenar valores
derivados. Decimal evita usar ponto flutuante binário para as notas.
Compare `is None` com `if not nota1`: a segunda forma trataria zero como ausente.
A média não é arredondada antes da classificação.

## 4. Formulários, autorização e templates

ModelForm cria campos e validações a partir do Model. Meta.fields lista explicitamente
os campos aceitos. Não confie apenas nas restrições visuais do HTML.
login_required exige identidade; user_passes_test(pode_editar) exige is_staff.
Ocultar um botão é só apresentação: o teste de autorização deve existir no servidor.
Nesta versão, leitor que tenta editar recebe redirecionamento para login.

base.html centraliza cabeçalho, navegação e mensagens. extends reutiliza esse layout;
block content define a parte variável; for percorre a coleção de registros.
csrf_token protege formulários POST; a proteção também vale para logout.
O escape automático do template ajuda a impedir que texto cadastrado vire HTML executável.

## 5. Onde os fundamentos de Python aparecem

| Conceito | Exemplo no projeto |
| --- | --- |
| Classes, atributos e herança | Models e ModelForms |
| Funções e parâmetros opcionais | salvar(request, entidade, pk=None) |
| Condicionais | nota ausente, método HTTP e formulário válido |
| Dicionários e tuplas | CADASTROS e retorno de configuracao |
| Laços e enumerate | comando dados_demo |
| Exceções | ProtectedError e Http404 |
| Modularização | models, forms, views e urls |

## 6. Atividade de leitura com respostas esperadas

1. Onde mudar a média mínima? Em Matricula.situacao; atualize requisitos e testes de fronteira.
2. Por que não gravar media? É derivada das notas e poderia ficar desatualizada.
3. Quem executa SQL? O ORM; o template apenas apresenta o resultado recebido.
4. Por que PROTECT? Para não apagar histórico acidentalmente por cascata.
5. Por que buscar registro com get_object_or_404? Para retornar 404 quando o ID não existe.
6. Por que usar um dicionário de cadastros? Para compartilhar o CRUD sem duplicar cinco fluxos.
7. Onde a autorização é aplicada? Nos decoradores das views de escrita, além dos botões.
8. Por que dados_demo não cria contas? Para evitar senha universal distribuída no código.

## 7. Pequena evolução proposta

Acrescente telefone opcional ao Aluno: escreva o requisito, altere Model e Form,
gere migração, teste valor vazio e preenchido, execute toda a suíte e documente.
Não confunda migrar o esquema com carregar registros. makemigrations gera a mudança;
migrate aplica a mudança ao banco. Entregue a migração junto do código.
