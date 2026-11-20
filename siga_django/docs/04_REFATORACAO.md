# 04 · Refatorar preservando comportamento

Refatoração melhora a estrutura sem mudar o comportamento observável.
Adicionar telefone é evolução de requisito; extrair uma função repetida é refatoração.
Antes de alterar, execute os testes e registre o resultado. Faça uma mudança pequena,
rode os mesmos testes, compare e registre o motivo.

## Exemplo: centralizar a regra de média

Uma versão ingênua repetiria `(nota1 + nota2) / 2` na view de listagem e na tela de
edição. A versão entregue usa Matricula.media. O template lê objeto.media e a
propriedade situacao reutiliza a mesma regra. Isso evita divergência entre telas.
Os casos de zero, ausência e média exatamente 6 protegem esse comportamento.

## Exercício seguro: extrair a operação de cálculo

1. Execute test_notas_limites_e_pendencia.
2. Crie academico/regras.py com a função abaixo.
3. Faça media delegar à função; mantenha a assinatura da propriedade.
4. Execute o teste isolado e a suíte inteira. A interface e as respostas devem permanecer iguais.

```python
from decimal import Decimal

def calcular_media(nota1, nota2):
    if nota1 is None or nota2 is None:
        return None
    return (nota1 + nota2) / Decimal('2')
```

Na propriedade, use `return calcular_media(self.nota1, self.nota2)` após importar
a função. Essa extração é um exercício proposto; a versão inicial mantém a regra
no Model para reduzir o número de arquivos. Não crie camadas sem uma necessidade.

## Exemplo de desempenho já aplicado

A listagem de matrículas usa select_related para trazer aluno, turma e disciplina
de uma vez. Sem isso, acessar as relações durante cada iteração pode gerar várias
consultas extras. Compare no shell com connection.queries e DEBUG=True, usando
listas novas de QuerySets em cada medição. Uma refatoração de desempenho deve
preservar o conteúdo apresentado e ser apoiada por medição.

Registro da alteração: problema observado; arquivo/função; mudança; comportamento
preservado; testes antes/depois; efeito e decisão de manter ou reverter.
