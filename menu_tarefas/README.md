# Menu de tarefas para uma equipe de serviços

Protótipo de terminal para registrar tarefas durante o turno de trabalho.

## Execução
```bash
python menu_tarefas.py
```

## Opções do menu
1. **Cadastrar tarefa**: título (obrigatório) e prioridade (baixa, média ou alta). A situação inicial é `pendente`.
2. **Listar tarefas**: mostra as tarefas numeradas a partir de 1.
3. **Atualizar situação**: marca uma tarefa existente como `concluída`, informando o número dela.
4. **Encerrar sistema**.

## Validações
- O título vazio é recusado.
- A prioridade fora de baixa, média ou alta é recusada.
- Um número de tarefa inexistente ou não numérico gera a mensagem "Tarefa inexistente."
- Uma opção de menu desconhecida gera a mensagem "Opção inválida".

## Limitações conhecidas
- Os dados ficam apenas em memória e são perdidos quando o programa é encerrado.
- Não é possível editar nem excluir tarefas.
