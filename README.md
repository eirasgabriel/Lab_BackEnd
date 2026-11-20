# Lab_BackEnd — Laboratório de Programação Back End

Atividades práticas (hands-on) da disciplina. 

| Semana | Pasta | Atividade | Como executar |
|---|---|---|---|
| 01 | `sistema_tarefas/` | Base reproduzível do Sistema de Gestão de Tarefas | `python main.py` |
| 02 | `cadastro_tarefa/` | Protótipo de cadastro de tarefa em terminal | `python cadastro_tarefa.py` |
| 03 | `menu_tarefas/` | Menu de tarefas para uma equipe de serviços | `python menu_tarefas.py` |
| 04 | `gerenciador_chamados/` | Gerenciador de chamados internos | `python gerenciador_chamados.py` |
| 05 | `controle_tarefas/` | Refatoração de um controle interno de tarefas | `python main.py` |
| 06 | `primeira_interface_web/` | Primeira interface web do Sistema de Gestão de Tarefas | `python manage.py runserver` |
| 10 | `siga_django/` | SIGA — integração e entrega com Django | `python manage.py migrate && python manage.py runserver` |

Entre na pasta da atividade (`cd nome_da_pasta`) antes de executar.

## Ambiente virtual (uma vez, na raiz)
```powershell
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r primeira_interface_web/requirements.txt
```
