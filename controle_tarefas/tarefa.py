# Semana 05 - Classe Tarefa: dados + comportamento de uma tarefa


class Tarefa:
    def __init__(self, titulo, descricao, prioridade):
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.situacao = "Pendente"

    def concluir(self):
        """Altera o estado da própria tarefa."""
        self.situacao = "Concluída"

    def exibir_resumo(self):
        """Devolve um texto; quem chama decide onde exibir."""
        return (
            f"Título: {self.titulo} | "
            f"Prioridade: {self.prioridade} | "
            f"Situação: {self.situacao}"
        )
