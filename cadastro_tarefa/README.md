

Lê título, prioridade, prazo e urgência de uma tarefa, calcula o esforço estimado
e mostra um resumo formatado.

## Execução
```bash
python cadastro_tarefa.py
```

## Regra de priorização
A tarefa é prioritária quando `prioridade >= 4` **ou** quando for urgente.
Esforço estimado = prazo × 1.2.

## Cenários testados
| Entrada | Prioritária |
|---|---|
| prioridade 5, prazo 3, urgente nao | True (prioridade alta) |
| prioridade 2, prazo 4.5, urgente sim | True (urgente) |
| prioridade 1, prazo 2, urgente nao | False |
