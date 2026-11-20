from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

app = FastAPI(title='API de Alunos')
Texto = Annotated[
    str, StringConstraints(strict=True, strip_whitespace=True, min_length=1)
]

class AlunoEntrada(BaseModel):
    nome: Texto
    curso: Texto

alunos = [{'id': 1, 'nome': 'Ana', 'curso': 'Engenharia de Software'}]

@app.get('/alunos')
def listar_alunos():
    return alunos

@app.post('/alunos', status_code=201)
def cadastrar_aluno(dados: AlunoEntrada):
    aluno = {'id': len(alunos) + 1, **dados.model_dump()}
    alunos.append(aluno)
    return aluno
