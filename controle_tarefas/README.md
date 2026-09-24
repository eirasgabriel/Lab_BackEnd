# Controle de Tarefas

Refatoração do protótipo procedural: cada tarefa agora é um objeto da classe
`Tarefa`, e as operações ficam em funções com responsabilidades claras.

## Execução
```bash
python main.py
```

## Organização
| Arquivo | Responsabilidade |
|---|---|
| `tarefa.py` | A classe `Tarefa`, com os atributos `titulo`, `descricao`, `prioridade` e `situacao`, e os métodos `concluir()` e `exibir_resumo()` |
| `servicos.py` | As funções `cadastrar_tarefa()`, `listar_tarefas()` e `filtrar_por_situacao()` |
| `main.py` | A integração e a demonstração, além de `ler_dados_tarefa()`, que cuida da interface de terminal |

## Funcionalidades demonstradas
- Cadastro de três tarefas.
- Conclusão de uma tarefa, que muda o estado do objeto.
- Listagem de todas as tarefas.
- Filtro das tarefas concluídas e das pendentes.
- Cadastro opcional de uma nova tarefa pelo terminal.
