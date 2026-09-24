# Gerenciador de chamados internos

Protótipo de terminal para consultar chamados de suporte, acompanhar as situações
e identificar as categorias atendidas. Os chamados ficam em uma lista de dicionários.

## Execução
```bash
python gerenciador_chamados.py
```

## O que o programa demonstra
1. A listagem de todos os chamados, com `for`.
2. O filtro por situação: `"aberto"` retorna resultados e `"cancelado"` mostra a mensagem de nenhum resultado.
3. A atualização por id: o id 3 é atualizado e o id 99 mostra "Chamado não encontrado."
4. As categorias sem repetição, com `set()`.

## Exemplo de saída
```
ID: 1
Título: Sem acesso ao sistema interno
Prioridade: alta
Situação: aberto
Categoria: acesso
------------------------------
...
=== CATEGORIAS ATENDIDAS ===
- acesso
- hardware
- rede
- software
```

## Autoria
_(preencha com o seu nome ou o nome da dupla)_
