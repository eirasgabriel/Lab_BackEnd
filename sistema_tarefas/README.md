# Sistema Web de Gestão de Tarefas

Projeto inicial para organização de tarefas. Base reproduzível: script executável,
ambiente virtual isolado, dependências registradas e controle de versão.

## Pré-requisito
- Python 3 instalado.
- Git instalado.

## Execução
Crie o ambiente virtual:
```bash
python -m venv .venv
```
Ative o ambiente virtual:
```bash
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
Execute o script:
```bash
python main.py
```

## Observações
- A pasta `.venv/` não é versionada (ver `.gitignore`).
- O `requirements.txt` foi gerado com `pip freeze > requirements.txt`.
