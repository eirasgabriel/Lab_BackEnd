# Semana 03 - Menu de tarefas para uma equipe de serviços
# Conceitos: while, if/elif/else, for, break, validação de entrada.

tarefas = []  # dados só em memória: são perdidos ao encerrar

while True:
    print("\n1 - Cadastrar tarefa")
    print("2 - Listar tarefas")
    print("3 - Atualizar situação")
    print("4 - Encerrar sistema")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        titulo = input("Título: ").strip()
        prioridade = input("Prioridade (baixa, média ou alta): ").strip().lower()
        if prioridade == "media":
            prioridade = "média"  # aceita digitação sem acento

        if titulo == "":
            print("O título não pode ficar vazio. Tarefa não cadastrada.")
        elif prioridade not in ("baixa", "média", "alta"):
            print("Prioridade inválida. Use baixa, média ou alta. Tarefa não cadastrada.")
        else:
            tarefas.append({
                "titulo": titulo,
                "prioridade": prioridade,
                "situacao": "pendente",
            })
            print("Tarefa cadastrada com sucesso.")

    elif opcao == "2":
        if len(tarefas) == 0:
            print("Nenhuma tarefa cadastrada.")
        else:
            numero = 1
            for tarefa in tarefas:
                print(f"{numero} - {tarefa['titulo']} | prioridade: {tarefa['prioridade']}"
                      f" | situação: {tarefa['situacao']}")
                numero += 1

    elif opcao == "3":
        entrada = input("Número da tarefa a concluir: ").strip()
        if entrada.isdigit():
            indice = int(entrada) - 1
            if 0 <= indice <= len(tarefas) - 1:
                tarefas[indice]["situacao"] = "concluída"
                print("Tarefa marcada como concluída.")
            else:
                print("Tarefa inexistente.")
        else:
            print("Tarefa inexistente.")

    elif opcao == "4":
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida. Escolha um número de 1 a 4.")
