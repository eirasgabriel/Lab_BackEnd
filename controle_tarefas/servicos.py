# Semana 05 - Funções de operação sobre a lista de tarefas


def cadastrar_tarefa(tarefas, titulo, descricao, prioridade, classe_tarefa):
    """Cria um objeto da classe recebida, inclui na lista e o devolve."""
    nova_tarefa = classe_tarefa(titulo, descricao, prioridade)
    tarefas.append(nova_tarefa)
    return nova_tarefa


def listar_tarefas(tarefas):
    """Apresenta as tarefas recebidas, numeradas a partir de 1."""
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    for indice, tarefa in enumerate(tarefas, start=1):
        print(f"{indice}. {tarefa.exibir_resumo()}")


def filtrar_por_situacao(tarefas, situacao):
    """Devolve uma NOVA lista com as tarefas daquela situação."""
    return [tarefa for tarefa in tarefas if tarefa.situacao == situacao]
