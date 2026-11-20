"""Testes automatizados com banco temporário, independente do banco de aula."""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase, Client
from django.urls import reverse
from .forms import AlunoForm, MatriculaForm
from .models import Aluno, Professor, Disciplina, Turma, Matricula

class SistemaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Uma base conhecida torna os resultados repetíveis.
        cls.editor = get_user_model().objects.create_user('editor', password='SenhaDeTeste123!', is_staff=True)
        cls.leitor = get_user_model().objects.create_user('leitor', password='SenhaDeTeste123!')
        cls.aluno = Aluno.objects.create(nome='Ana', matricula='A1', email='ana@example.com')
        professor = Professor.objects.create(nome='Docente', email='doc@example.com')
        disciplina = Disciplina.objects.create(nome='Back End', codigo='BE')
        cls.turma = Turma.objects.create(codigo='T1', disciplina=disciplina, professor=professor)

    def setUp(self):
        self.client.force_login(self.editor)

    def test_visitante_precisa_login(self):
        self.client.logout()
        self.assertRedirects(self.client.get('/alunos/'), '/entrar/?next=/alunos/')

    def test_login_e_logout(self):
        self.client.logout()
        self.assertTrue(self.client.login(username='editor', password='SenhaDeTeste123!'))
        self.assertEqual(self.client.get('/').status_code, 200)
        self.client.post('/sair/')
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_leitor_consulta_mas_nao_altera(self):
        self.client.force_login(self.leitor)
        self.assertEqual(self.client.get('/alunos/').status_code, 200)
        for url in ['/alunos/novo/', f'/alunos/{self.aluno.pk}/editar/', f'/alunos/{self.aluno.pk}/excluir/']:
            self.assertEqual(self.client.post(url, {'nome': 'Intruso'}).status_code, 302)
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.nome, 'Ana')

    def test_crud_aluno(self):
        resposta = self.client.post('/alunos/novo/', {'nome': 'Bia', 'matricula': 'B2', 'email': 'bia@example.com'})
        self.assertRedirects(resposta, '/alunos/')
        aluno = Aluno.objects.get(matricula='B2')
        self.client.post(f'/alunos/{aluno.pk}/editar/', {'nome': 'Beatriz', 'matricula': 'B2', 'email': 'bia@example.com'})
        aluno.refresh_from_db()
        self.assertEqual(aluno.nome, 'Beatriz')
        self.assertContains(self.client.get('/alunos/?q=Beatriz'), 'Beatriz')
        self.client.get(f'/alunos/{aluno.pk}/excluir/')
        self.assertTrue(Aluno.objects.filter(pk=aluno.pk).exists())
        self.client.post(f'/alunos/{aluno.pk}/excluir/')
        self.assertFalse(Aluno.objects.filter(pk=aluno.pk).exists())

    def test_formulario_invalido_nao_persiste(self):
        total = Aluno.objects.count()
        resposta = self.client.post('/alunos/novo/', {'nome': '', 'matricula': 'X', 'email': 'invalido'})
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.context['form'].errors)
        self.assertEqual(Aluno.objects.count(), total)

    def test_matricula_aluno_unica(self):
        form = AlunoForm(data={'nome': 'Outra', 'matricula': 'A1', 'email': 'outra@example.com'})
        self.assertFalse(form.is_valid())
        self.assertIn('matricula', form.errors)

    def test_notas_limites_e_pendencia(self):
        for n1, n2, media, situacao in [
            (None, 10, None, 'Pendente'), (0, 0, Decimal('0'), 'Reprovado'),
            (5, 7, Decimal('6'), 'Aprovado'), (5, 6, Decimal('5.5'), 'Reprovado'),
            (10, 10, Decimal('10'), 'Aprovado'),
        ]:
            with self.subTest(n1=n1, n2=n2):
                objeto = Matricula(nota1=n1, nota2=n2)
                self.assertEqual(objeto.media, media)
                self.assertEqual(objeto.situacao, situacao)

    def test_notas_invalidas(self):
        for campo in ['nota1', 'nota2']:
            for valor in ['-0.01', '10.01', 'abc']:
                with self.subTest(campo=campo, valor=valor):
                    dados = {'aluno': self.aluno.pk, 'turma': self.turma.pk, campo: valor}
                    form = MatriculaForm(data=dados)
                    self.assertFalse(form.is_valid())
                    self.assertIn(campo, form.errors)

    def test_fluxo_matricula_e_boletim(self):
        dados = {'aluno': self.aluno.pk, 'turma': self.turma.pk, 'nota1': '5', 'nota2': '7'}
        self.assertRedirects(self.client.post('/matriculas/novo/', dados), '/matriculas/')
        self.assertContains(self.client.get('/matriculas/'), 'Aprovado')
        self.assertEqual(Matricula.objects.get().media, Decimal('6'))
        resposta = self.client.post('/matriculas/novo/', dados)
        self.assertTrue(resposta.context['form'].errors)
        self.assertEqual(Matricula.objects.count(), 1)

    def test_protecao_de_relacionamentos(self):
        Matricula.objects.create(aluno=self.aluno, turma=self.turma)
        resposta = self.client.post(f'/alunos/{self.aluno.pk}/excluir/', follow=True)
        self.assertContains(resposta, 'existem registros vinculados')
        self.assertTrue(Aluno.objects.filter(pk=self.aluno.pk).exists())

    def test_banco_rejeita_nota_invalida(self):
        # save() não executa full_clean(): a restrição também protege o banco.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Matricula.objects.create(aluno=self.aluno, turma=self.turma, nota1=11)

    def test_banco_rejeita_matricula_duplicada(self):
        Matricula.objects.create(aluno=self.aluno, turma=self.turma)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Matricula.objects.create(aluno=self.aluno, turma=self.turma)

    def test_rotas_inexistentes(self):
        self.assertEqual(self.client.get('/alunos/99999/editar/').status_code, 404)
        self.assertEqual(self.client.get('/inexistente/').status_code, 404)

    def test_csrf_obrigatorio(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.editor)
        self.assertEqual(cliente.post('/alunos/novo/', {}).status_code, 403)

    def test_cadastros_relacionados(self):
        for entidade, dados in [
            ('professores', {'nome': 'Outro', 'email': 'outro@example.com'}),
            ('disciplinas', {'nome': 'Redes', 'codigo': 'RE'}),
            ('turmas', {'codigo': 'T2', 'disciplina': self.turma.disciplina_id, 'professor': self.turma.professor_id, 'semestre': '2026.2'}),
        ]:
            with self.subTest(entidade=entidade):
                self.assertRedirects(self.client.post(f'/{entidade}/novo/', dados), f'/{entidade}/')
                self.assertEqual(self.client.get(f'/{entidade}/').status_code, 200)

    def test_demo_idempotente(self):
        call_command('dados_demo', verbosity=0)
        totais = [m.objects.count() for m in [Aluno, Professor, Disciplina, Turma, Matricula]]
        call_command('dados_demo', verbosity=0)
        self.assertEqual(totais, [m.objects.count() for m in [Aluno, Professor, Disciplina, Turma, Matricula]])
