from django.test import TestCase
from django.urls import reverse


class RotasTests(TestCase):
    def test_inicio(self):
        resposta = self.client.get(reverse("inicio"))
        self.assertEqual(resposta.status_code, 200)

    def test_lista_mostra_tarefas(self):
        resposta = self.client.get(reverse("lista_tarefas"))
        self.assertContains(resposta, "Criar rotas com urls.py")

    def test_pendentes_nao_mostra_concluidas(self):
        resposta = self.client.get(reverse("tarefas_pendentes"))
        self.assertNotContains(resposta, "Escrever README")
