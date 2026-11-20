"""Teste HTTP real. Inicie as duas APIs antes de executar."""
import json
import urllib.request
import urllib.error
import http.cookiejar

def testar(porta, csrf=False):
    url = f'http://127.0.0.1:{porta}/alunos'
    cookies = http.cookiejar.CookieJar()
    cliente = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))
    def enviar(metodo='GET', dados=None):
        cabecalhos = {'Content-Type': 'application/json'}
        if csrf:
            cabecalhos.update({'X-CSRFToken': next((c.value for c in cookies if c.name == 'csrftoken'), '')})
        corpo = None if dados is None else json.dumps(dados).encode('utf-8')
        req = urllib.request.Request(url, data=corpo, headers=cabecalhos, method=metodo)
        try:
            resp = cliente.open(req, timeout=5)
        except urllib.error.HTTPError as erro:
            resp = erro
        with resp:
            status, texto = resp.code, resp.read().decode('utf-8')
        print(metodo, porta, status, texto)
        return status, json.loads(texto)
    status, antes = enviar()
    assert status == 200
    status, novo = enviar('POST', {'nome':'  Teste  ', 'curso':'Backend'})
    assert status == 201 and novo['nome'] == 'Teste'
    status, depois = enviar()
    assert len(depois) == len(antes) + 1
    status, _ = enviar('POST', {'nome':'   ', 'curso':'Backend'})
    assert status == (400 if csrf else 422)
    _, final = enviar()
    assert len(final) == len(depois)

try:
    testar(8000, csrf=True)
    testar(8001)
except urllib.error.URLError:
    raise SystemExit('Conexão indisponível. Inicie as duas APIs nas portas 8000 e 8001.')
print('Verificações concluídas. O teste incluiu um aluno em cada servidor.')
