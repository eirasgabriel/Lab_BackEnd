# Aula prática: APIs com Django e FastAPI

**Disciplina:** Laboratório de Programação Back End  
**Professor:** Ralfh Varges Ansuattigui

## O que você vai fazer?

Você vai executar duas versões de um cadastro de alunos: uma com Django e outra com FastAPI. Os códigos estão prontos para executar.

Primeiro, consulte e cadastre alunos. Depois, envie dados inválidos e localize no código o que explica as respostas.

## 1. Abra o projeto

1. Descompacte o ZIP recebido.
2. Abra o VS Code e clique em **Arquivo > Abrir Pasta**.
3. Selecione a pasta **Projeto_VSCode**.

**Confira:** na lateral esquerda devem aparecer `django_api`, `fastapi_api`, `scripts` e este `README.md`.

Para ler este guia formatado, abra o README e pressione **Ctrl+Shift+V**.

## 2. Prepare o ambiente

Você precisa de **Python 3.12 ou superior** instalado e de internet para instalar as bibliotecas.

1. Clique em **Terminal > Executar Tarefa**.
2. Selecione **1. Preparar ambiente**.
3. Aguarde até aparecer **“Ambiente pronto”**. A primeira execução pode levar alguns minutos.

Essa tarefa cria a pasta `.venv`, que guarda o ambiente Python da aula, e instala as bibliotecas necessárias. Não é necessário ativar esse ambiente manualmente.

**Só avance quando a preparação terminar sem erros.** Em outro dia, no mesmo computador e na mesma pasta, você pode começar pela etapa 3 se o ambiente já estiver preparado.

## 3. Inicie os dois servidores

Um servidor é o programa que fica aguardando solicitações. Vamos iniciar um para cada versão.

1. Clique em **Terminal > Executar Tarefa > 2. Iniciar Django**.
2. Aguarde o endereço `http://127.0.0.1:8000/` aparecer no terminal.
3. Clique em **Terminal > Executar Tarefa > 3. Iniciar FastAPI**.
4. Aguarde aparecer o endereço `http://127.0.0.1:8001` e a mensagem de inicialização concluída.

**Mantenha os dois terminais em execução.** Eles não precisam voltar a mostrar o cursor para que você continue. Cada servidor fica em seu próprio terminal.

| Versão | Endereço para consultar alunos |
|---|---|
| Django | http://127.0.0.1:8000/alunos |
| FastAPI | http://127.0.0.1:8001/alunos |

`127.0.0.1` é o seu computador. As portas **8000** e **8001** permitem acessar os dois servidores separadamente.

## 4. Consulte os alunos

Abra cada endereço da tabela em uma aba do navegador. Nas duas versões, a lista inicial deve apresentar:

```json
[
  {
    "id": 1,
    "nome": "Ana",
    "curso": "Engenharia de Software"
  }
]
```

A aparência pode variar conforme o navegador. Os dados devem ser os mesmos.

Ao abrir esses endereços, o navegador envia uma requisição **GET**, usada aqui para consultar dados. A resposta utiliza **JSON**, um formato de texto para troca de dados entre programas.

## 5. Cadastre um aluno no FastAPI

Vamos usar a documentação interativa, que permite enviar solicitações pela própria página.

1. Abra http://127.0.0.1:8001/docs.
2. Clique em **POST /alunos** e depois em **Try it out**.
3. No campo de entrada, substitua o conteúdo por:

```json
{
  "nome": "Bruno",
  "curso": "Engenharia de Software"
}
```

4. Clique em **Execute**.
5. Procure a seção **Server response**.

**Resultado esperado:** código **201**, indicando criação, e o aluno com um `id` gerado pelo servidor. O primeiro cadastro após iniciar recebe `id` igual a 2.

Volte a http://127.0.0.1:8001/alunos e atualize a página. Bruno deve aparecer na lista.

**Observe:** o cadastro foi realizado somente no FastAPI. A lista Django é independente.

## 6. Execute os testes nas duas versões

O arquivo `scripts/testar.ps1` contém os comandos para consultar, cadastrar e testar dados inválidos nas duas APIs.

1. Abra `scripts/testar.ps1` no VS Code.
2. Clique em **Terminal > Novo Terminal**, mantendo os dois servidores em execução.
3. Confira se o novo terminal é **PowerShell**. Se precisar, escolha esse perfil na seta ao lado do botão **+** do terminal.
4. Copie o conteúdo completo de `scripts/testar.ps1` e cole nesse terminal. Se houver um aviso de colagem de várias linhas, confira o conteúdo e prossiga.
5. Pressione **Enter** e observe os resultados.

Não é necessário alterar a política de execução: você está colando os comandos no terminal.

| Teste | O que observar |
|---|---|
| Consulta | Lista de alunos |
| Cadastro de Bruno | Novo aluno com identificador gerado pelo servidor |
| Nova consulta | A lista contém o registro incluído |
| Nome contendo apenas espaços | Erro **400** no Django e **422** no FastAPI |

Os comandos normalmente mostram o conteúdo das respostas de sucesso. O tratamento de erros mostra o código e os detalhes das respostas inválidas.

**Por que há comandos de cookie e token no início?** O Django mantém uma proteção chamada CSRF. Esses comandos obtêm e enviam as informações necessárias para realizar o cadastro. Mantenha o bloco completo e na ordem fornecida.

**Repetir o teste cadastra Bruno novamente.** Se você já fez a etapa 5, o identificador do próximo aluno no FastAPI será maior que 2. Isso é esperado.

### Teste automático opcional

Com as duas APIs iniciadas, selecione **Terminal > Executar Tarefa > 4. Testar as duas APIs**.

A tarefa confere consulta, cadastro, remoção de espaços nas extremidades e rejeição de nome vazio. Ao final, deve aparecer **“Verificações concluídas”**.

Ela adiciona um aluno chamado `Teste` em cada versão. Para restaurar os dados iniciais, encerre e reinicie os servidores, conforme a etapa 9.

## 7. Investigue o código

Procure os elementos indicados e relacione-os aos resultados observados.

| O que procurar | Django | FastAPI |
|---|---|---|
| Caminho `/alunos` | `django_api/config/urls.py` | Decoradores em `fastapi_api/main.py` |
| Consulta da lista | Condição GET em `django_api/alunos/views.py` | Função `listar_alunos` em `fastapi_api/main.py` |
| Validação dos campos | Função `validar` em `django_api/alunos/views.py` | Modelo `AlunoEntrada` e definição `Texto` em `fastapi_api/main.py` |
| Inclusão do aluno | `alunos.append(aluno)` em `django_api/alunos/views.py` | `alunos.append(aluno)` em `fastapi_api/main.py` |
| Resposta do cadastro | `JsonResponse(aluno, status=201)` | `return aluno`, com `status_code=201` no decorador |

Pergunta para orientar a leitura: **qual trecho impede que um nome contendo apenas espaços entre na lista?**

## 8. Preencha e entregue a atividade

1. Abra **respostas.md** e preencha nomes e matrículas.
2. Responda aos quatro itens seguindo **Atividade_Alunos.pdf**.
3. Registre os dados, códigos e identificadores realmente observados.
4. Ao citar código, informe arquivo, função ou classe e um trecho curto.
5. Salve com **Ctrl+S** e entregue conforme a orientação do professor.

## 9. Encerre ou reinicie

Selecione o terminal do Django e pressione **Ctrl+C**. Faça o mesmo no terminal do FastAPI.

Para iniciar novamente, execute as tarefas **2. Iniciar Django** e **3. Iniciar FastAPI**.

**Ao reiniciar, os cadastros novos serão apagados.** Nesta aula, os dados ficam em listas na memória. Não há banco de dados. Cada versão volta a apresentar somente Ana.

## Se algo não funcionar

| Situação | Como resolver |
|---|---|
| As tarefas não aparecem | Abra a pasta **Projeto_VSCode**, em vez da pasta que contém todos os materiais. |
| Comando `py` não encontrado | Confirme a instalação Python com o professor. Se `python` funcionar, prepare usando `python scripts/preparar.py` no terminal. |
| Falha na instalação | Confira a conexão e aguarde a preparação terminar sem erros. |
| `ModuleNotFoundError` | Execute a preparação e inicie as APIs pelas tarefas fornecidas. |
| Navegador não conecta | Confira se o servidor continua em execução e se o endereço e a porta estão corretos. |
| Erro 404 | Use o endereço completo com `/alunos`, sem barra final. A página inicial `/` não foi criada. |
| Erro 403 no Django | Execute o bloco de teste completo desde o início, para obter e enviar cookie e token. Use sempre `127.0.0.1`. |
| Porta já em uso | Encerre o servidor anterior com **Ctrl+C** antes de iniciar outro. |
| Mais alunos que no exemplo | Os testes anteriores incluíram registros. Reinicie para restaurar a lista inicial. |

## Complemento: comandos manuais

Utilize esta seção se o professor orientar. Os comandos fazem o mesmo que as tarefas do VS Code. Execute-os na pasta **Projeto_VSCode**, com um terminal para cada servidor.

Preparar:

```powershell
py scripts/preparar.py
```

Iniciar Django:

```powershell
.\.venv\Scripts\python.exe django_api/manage.py runserver 127.0.0.1:8000 --noreload
```

Iniciar FastAPI em outro terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir fastapi_api --host 127.0.0.1 --port 8001
```

## Sobre esta demonstração

- `requirements.txt` lista as bibliotecas. O preparador informa as versões instaladas.
- Os exemplos não possuem banco, interface própria ou autenticação de usuários.
- As configurações e o cálculo de identificadores foram simplificados para execução local, sequencial e sem exclusões.
- Os códigos 400 e 422 refletem o tratamento escolhido para cada versão.
- Consulte `VALIDACAO.md` e o relatório do pacote para conhecer os testes realizados na preparação.
