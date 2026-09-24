# Semana 05 - Programa principal: integra a classe e as funções.
# A leitura do terminal (interface) fica separada das regras (servicos.py).

from tarefa import Tarefa
from servicos import cadastrar_tarefa, filtrar_por_situacao, listar_tarefas


def ler_dados_tarefa():
    """Interface de terminal: apenas lê os dados."""
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    prioridade = input("Prioridade: ")
    return titulo, descricao, prioridade


def main():
    tarefas = []

    # Demonstração com três tarefas
    cadastrar_tarefa(tarefas, "Revisar chamados",
                     "Verificar chamados pendentes da equipe", "Alta", Tarefa)
    cadastrar_tarefa(tarefas, "Atualizar manual interno",
                     "Ajustar instruções de atendimento", "Média", Tarefa)
    cadastrar_tarefa(tarefas, "Planejar reunião",
                     "Preparar pauta da reunião semanal", "Baixa", Tarefa)

    # Demonstração da mudança de estado
    tarefas[0].concluir()

    print("Todas as tarefas:")
    listar_tarefas(tarefas)

    print("\nTarefas concluídas:")
    listar_tarefas(filtrar_por_situacao(tarefas, "Concluída"))

    print("\nTarefas pendentes:")
    listar_tarefas(filtrar_por_situacao(tarefas, "Pendente"))

    # Uso opcional pelo terminal
    resposta = input("\nDeseja cadastrar uma nova tarefa? (s/n): ").strip().lower()
    if resposta == "s":
        titulo, descricao, prioridade = ler_dados_tarefa()
        cadastrar_tarefa(tarefas, titulo, descricao, prioridade, Tarefa)
        print("\nLista atualizada:")
        listar_tarefas(tarefas)


if __name__ == "__main__":
    main()
