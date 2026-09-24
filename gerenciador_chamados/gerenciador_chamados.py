# Semana 04 - Gerenciador de chamados internos
# Estrutura: lista de dicionários. Também usa set para categorias únicas.

chamados = [
    {"id": 1, "titulo": "Sem acesso ao sistema interno", "prioridade": "alta",
     "situacao": "aberto", "categoria": "acesso"},
    {"id": 2, "titulo": "Impressora sem conexão", "prioridade": "média",
     "situacao": "em atendimento", "categoria": "hardware"},
    {"id": 3, "titulo": "Senha de e-mail expirada", "prioridade": "média",
     "situacao": "aberto", "categoria": "acesso"},
    {"id": 4, "titulo": "Monitor com falha de imagem", "prioridade": "baixa",
     "situacao": "resolvido", "categoria": "hardware"},
    {"id": 5, "titulo": "Instalação de software de planilhas", "prioridade": "baixa",
     "situacao": "aberto", "categoria": "software"},
    {"id": 6, "titulo": "Rede lenta no setor financeiro", "prioridade": "alta",
     "situacao": "em atendimento", "categoria": "rede"},
]

SEPARADOR = "-" * 30

# ---------------------------------------------------------------
# 1) Listagem de todos os chamados
# ---------------------------------------------------------------
print("=== TODOS OS CHAMADOS ===")
for chamado in chamados:
    print(f"ID: {chamado['id']}")
    print(f"Título: {chamado['titulo']}")
    print(f"Prioridade: {chamado['prioridade']}")
    print(f"Situação: {chamado['situacao']}")
    print(f"Categoria: {chamado['categoria']}")
    print(SEPARADOR)

# ---------------------------------------------------------------
# 2) Filtro por situação (testado com um caso existente e um inexistente)
# ---------------------------------------------------------------
for situacao_desejada in ("aberto", "cancelado"):
    print(f"\n=== CHAMADOS COM SITUAÇÃO '{situacao_desejada}' ===")
    encontrou_chamado = False
    for chamado in chamados:
        if chamado["situacao"] == situacao_desejada:
            print(f"[{chamado['id']}] {chamado['titulo']} ({chamado['prioridade']})")
            encontrou_chamado = True
    if not encontrou_chamado:
        print(f"Nenhum chamado encontrado com a situação '{situacao_desejada}'.")

# ---------------------------------------------------------------
# 3) Atualização da situação por id (testado com id existente e inexistente)
# ---------------------------------------------------------------
testes_atualizacao = [(3, "resolvido"), (99, "resolvido")]
for id_procurado, nova_situacao in testes_atualizacao:
    print(f"\n=== ATUALIZAR CHAMADO {id_procurado} PARA '{nova_situacao}' ===")
    encontrou_id = False
    for chamado in chamados:
        if chamado["id"] == id_procurado:
            chamado["situacao"] = nova_situacao
            encontrou_id = True
            print(f"Chamado {id_procurado} atualizado para '{nova_situacao}'.")
            break  # o id é único: não precisa continuar procurando
    if not encontrou_id:
        print("Chamado não encontrado.")

# ---------------------------------------------------------------
# 4) Categorias sem repetição (set)
# ---------------------------------------------------------------
categorias = set()
for chamado in chamados:
    categorias.add(chamado["categoria"])

print("\n=== CATEGORIAS ATENDIDAS ===")
for categoria in sorted(categorias):
    print(f"- {categoria}")
print(f"Total de categorias: {len(categorias)}")
