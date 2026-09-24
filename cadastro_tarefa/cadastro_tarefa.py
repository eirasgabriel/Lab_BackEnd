# Semana 02 - Protótipo de cadastro de tarefa em terminal
# Usa apenas variáveis, tipos, conversões, operadores, input(), print() e f-strings.

print("=== Cadastro de Tarefa ===")

# Entrada de dados (input sempre devolve texto)
titulo = input("Título da tarefa: ")
prioridade = int(input("Prioridade (1 a 5): "))
prazo_horas = float(input("Prazo estimado em horas: "))
resposta_urgencia = input("A tarefa é urgente? (sim/nao): ")

# Conversão da resposta em booleano por comparação
urgente = resposta_urgencia.strip().lower() == "sim"

# Cálculos e expressões
fator_esforco = 1.2
esforco_estimado = prazo_horas * fator_esforco
prioridade_alta = prioridade >= 4             # comparação com valor de referência
prioritaria = prioridade_alta or urgente      # expressão lógica

# Resumo formatado
print("\n=== Resumo da Tarefa ===")
print(f"Título: {titulo}")
print(f"Prioridade: {prioridade}")
print(f"Prazo estimado: {prazo_horas:.1f} horas")
print(f"Urgente: {urgente}")
print(f"Esforço estimado (fator {fator_esforco}): {esforco_estimado:.2f} horas")
print(f"Prioridade alta (>= 4): {prioridade_alta}")
print(f"Tratar como prioritária: {prioritaria}")
