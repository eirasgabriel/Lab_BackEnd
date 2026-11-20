"""Testes dos models e das views da aplicação tarefas.

Cada teste roda em um banco de teste criado pelo Django, separado do
db.sqlite3 local; por isso os dados são criados aqui, sem fixture.
"""
from datetime import date

from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Tarefa


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.estudos = Categoria.objects.create(nome="Estudos")
        cls.pessoal = Categoria.objects.create(nome="Pessoal")
        cls.tarefa = Tarefa.objects.create(
            titulo="Revisar models do Django",
            data_prevista=date(2026, 11, 21),
            categoria=cls.estudos,
        )
        Tarefa.objects.create(
            titulo="Organizar documentos",
            data_prevista=date(2026, 11, 25),
            situacao=Tarefa.Situacao.CONCLUIDA,
            categoria=cls.pessoal,
        )

    def test_str_da_categoria_e_da_tarefa(self):
        self.assertEqual(str(self.estudos), "Estudos")
        self.assertEqual(str(self.tarefa), "Revisar models do Django")

    def test_valores_padrao(self):
        self.assertEqual(self.tarefa.prioridade, Tarefa.Prioridade.MEDIA)
        self.assertEqual(self.tarefa.situacao, Tarefa.Situacao.PENDENTE)

    def test_descricao_pode_ficar_vazia(self):
        self.assertEqual(self.tarefa.descricao, "")
        self.tarefa.full_clean()  # não levanta ValidationError

    def test_concluir_tarefa_persiste_no_banco(self):
        self.tarefa.situacao = Tarefa.Situacao.CONCLUIDA
        self.tarefa.save()
        recarregada = Tarefa.objects.get(pk=self.tarefa.pk)
        self.assertEqual(recarregada.situacao, Tarefa.Situacao.CONCLUIDA)

    def test_categoria_com_tarefas_nao_pode_ser_excluida(self):
        with self.assertRaises(ProtectedError):
            self.estudos.delete()
        self.assertTrue(Categoria.objects.filter(pk=self.estudos.pk).exists())

    def test_filtro_por_situacao(self):
        pendentes = Tarefa.objects.filter(situacao=Tarefa.Situacao.PENDENTE)
        self.assertQuerySetEqual(pendentes, [self.tarefa])

    def test_filtro_por_categoria(self):
        da_categoria = Tarefa.objects.filter(categoria__nome="Pessoal")
        self.assertQuerySetEqual(da_categoria, ["Organizar documentos"], transform=str)
        self.assertQuerySetEqual(self.estudos.tarefa_set.all(), [self.tarefa])


class ViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        estudos = Categoria.objects.create(nome="Estudos")
        pessoal = Categoria.objects.create(nome="Pessoal")
        # Criadas fora da ordem de data para testar a ordenação da listagem.
        Tarefa.objects.create(
            titulo="Tarefa tardia",
            data_prevista=date(2026, 12, 10),
            categoria=pessoal,
        )
        Tarefa.objects.create(
            titulo="Tarefa concluída",
            data_prevista=date(2026, 11, 18),
            situacao=Tarefa.Situacao.CONCLUIDA,
            categoria=estudos,
        )
        Tarefa.objects.create(
            titulo="Tarefa próxima",
            data_prevista=date(2026, 11, 21),
            prioridade=Tarefa.Prioridade.ALTA,
            categoria=estudos,
        )

    def test_inicio_mostra_total_do_banco(self):
        resposta = self.client.get(reverse("inicio"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Existem 3 tarefas cadastradas.")

    def test_lista_mostra_tarefas_com_categoria_e_data(self):
        resposta = self.client.get(reverse("lista_tarefas"))
        self.assertEqual(resposta.status_code, 200)
        for titulo in ("Tarefa tardia", "Tarefa concluída", "Tarefa próxima"):
            self.assertContains(resposta, titulo)
        self.assertContains(resposta, "<td>Pessoal</td>", html=True)
        self.assertContains(resposta, "<td>21/11/2026</td>", html=True)
        self.assertContains(resposta, "<td>Alta</td>", html=True)
        self.assertContains(resposta, "Concluída")

    def test_lista_ordenada_por_data_prevista(self):
        resposta = self.client.get(reverse("lista_tarefas"))
        titulos = [t.titulo for t in resposta.context["tarefas"]]
        self.assertEqual(titulos, ["Tarefa concluída", "Tarefa próxima", "Tarefa tardia"])

    def test_pendentes_nao_mostra_concluidas(self):
        resposta = self.client.get(reverse("tarefas_pendentes"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Tarefa próxima")
        self.assertContains(resposta, "Tarefa tardia")
        self.assertNotContains(resposta, "Tarefa concluída")

    def test_lista_vazia_mostra_mensagem(self):
        Tarefa.objects.all().delete()
        resposta = self.client.get(reverse("lista_tarefas"))
        self.assertContains(resposta, "Nenhuma tarefa cadastrada.")

    def test_sobre(self):
        resposta = self.client.get(reverse("sobre"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Sistema de Gestão de Tarefas")
