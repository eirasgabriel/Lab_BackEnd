import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

alunos = [{'id': 1, 'nome': 'Ana', 'curso': 'Engenharia de Software'}]

def validar(dados):
    if not isinstance(dados, dict):
        return None
    resultado = {}
    for campo in ('nome', 'curso'):
        valor = dados.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            return None
        resultado[campo] = valor.strip()
    return resultado

@ensure_csrf_cookie
@require_http_methods(['GET', 'POST'])
def alunos_view(request):
    if request.method == 'GET':
        return JsonResponse(alunos, safe=False)
    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'erro': 'JSON invalido.'}, status=400)
    dados_validos = validar(dados)
    if dados_validos is None:
        return JsonResponse(
            {'erro': 'Nome e curso devem ser textos nao vazios.'}, status=400
        )
    aluno = {'id': len(alunos) + 1, **dados_validos}
    alunos.append(aluno)
    return JsonResponse(aluno, status=201)
