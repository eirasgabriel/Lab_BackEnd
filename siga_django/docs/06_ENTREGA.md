# 06 · Integração e entrega verificável

Integração reúne os componentes e comprova o fluxo completo. Entrega fornece
código, dependências, migrações e instruções para outra pessoa executar.
O foco desta atividade é uma entrega local reproduzível; não exige hospedagem.

## Definição de pronto

- Requisitos implementados e limitações declaradas.
- check sem erros; migrações sem pendências; suíte aprovada.
- Fluxo manual com editor e leitor conferido no navegador.
- README seguido em uma pasta nova por outro integrante.
- Migrações e requirements incluídos; banco e ambiente virtual excluídos.
- Documentação, evidências e retrospectiva atualizadas.
- ZIP abre na IDE e contém manage.py na pasta principal do projeto.

## Sequência de integração em grupo

Antes de integrar: combine requisito, campo ou função alterada e critério de teste.
Trabalhe em ramo próprio se o grupo usar Git. Revise diferenças, integre uma
mudança por vez, resolva conflitos e execute check, verificação de migrações e testes.
Registre a versão entregue e não inclua senhas, .venv ou db.sqlite3.

## Integração contínua opcional

O arquivo .github/workflows/testes.yml executa instalação, check, verificação de
migrações e testes em push e pull request, caso o grupo use GitHub.
É um exemplo de CI: não publica a aplicação. A execução remota depende do repositório.

## Publicação futura

Esta configuração é de desenvolvimento. Antes de hospedar: selecionar versão
suportada e atualizada das dependências, retirar SECRET_KEY do código, definir
DEBUG=False e ALLOWED_HOSTS, configurar HTTPS/cookies, arquivos estáticos,
servidor WSGI/ASGI adequado e banco com backup, restringir permissões e executar
`python manage.py check --deploy` com a configuração de produção.
runserver não é servidor de produção. Não exponha o laboratório com dados reais.

## Registro de entrega

Versão: ____ · Data: ____ · Integrantes: ____ · Python/Django: ____
Comandos executados e resultados: ____
Testes exploratórios executados: ____
Requisitos não atendidos ou limitações: ____
Refatoração e evidência antes/depois: ____
Próximas ações e responsáveis: ____
