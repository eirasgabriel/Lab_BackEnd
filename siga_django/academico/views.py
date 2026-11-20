"""Views funcionais: recebem HTTP, coordenam operações e devolvem respostas."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.deletion import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .models import Aluno, Professor, Disciplina, Turma, Matricula
from .forms import AlunoForm, ProfessorForm, DisciplinaForm, TurmaForm, MatriculaForm

# Uma lista explícita evita escolher classes a partir de texto arbitrário da URL.
CADASTROS = {
    'alunos': (Aluno, AlunoForm, 'Alunos'),
    'professores': (Professor, ProfessorForm, 'Professores'),
    'disciplinas': (Disciplina, DisciplinaForm, 'Disciplinas'),
    'turmas': (Turma, TurmaForm, 'Turmas'),
    'matriculas': (Matricula, MatriculaForm, 'Matrículas e notas'),
}

def configuracao(entidade):
    if entidade not in CADASTROS:
        raise Http404('Cadastro inexistente')
    return CADASTROS[entidade]

def pode_editar(user):
    return user.is_staff

@login_required
def painel(request):
    return render(request, 'academico/painel.html', {
        'total_alunos': Aluno.objects.count(),
        'total_turmas': Turma.objects.count(),
        'total_matriculas': Matricula.objects.count(),
    })

@login_required
def listar(request, entidade):
    model, form_class, titulo = configuracao(entidade)
    objetos = model.objects.all().order_by('pk')
    busca = request.GET.get('q', '').strip()
    if entidade == 'alunos' and busca:
        objetos = objetos.filter(nome__icontains=busca)
    if entidade == 'matriculas':
        # Carrega relações na mesma consulta, evitando consultas dentro do loop.
        objetos = objetos.select_related('aluno', 'turma', 'turma__disciplina')
    return render(request, 'academico/lista.html', {
        'objetos': objetos, 'entidade': entidade, 'titulo': titulo, 'busca': busca,
    })

@login_required
@user_passes_test(pode_editar)
@require_http_methods(['GET', 'POST'])
def salvar(request, entidade, pk=None):
    model, form_class, titulo = configuracao(entidade)
    objeto = get_object_or_404(model, pk=pk) if pk is not None else None
    # Em GET o formulário é vazio/preenchido; em POST recebe os dados enviados.
    form = form_class(request.POST if request.method == 'POST' else None, instance=objeto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Registro salvo.')
        return redirect('listar', entidade=entidade)
    return render(request, 'academico/formulario.html', {'form': form, 'titulo': titulo, 'entidade': entidade})

@login_required
@user_passes_test(pode_editar)
@require_http_methods(['GET', 'POST'])
def excluir(request, entidade, pk):
    model, form_class, titulo = configuracao(entidade)
    objeto = get_object_or_404(model, pk=pk)
    # GET apenas confirma. A alteração do banco exige POST e token CSRF.
    if request.method == 'POST':
        try:
            objeto.delete()
            messages.success(request, 'Registro excluído.')
        except ProtectedError:
            messages.error(request, 'Não é possível excluir: existem registros vinculados.')
        return redirect('listar', entidade=entidade)
    return render(request, 'academico/excluir.html', {'objeto': objeto, 'entidade': entidade})
