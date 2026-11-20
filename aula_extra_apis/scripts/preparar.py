import subprocess
import sys
from pathlib import Path
raiz = Path(__file__).resolve().parents[1]
if sys.version_info < (3, 12):
    raise SystemExit('Utilize Python 3.12 ou superior.')
ambiente = raiz / '.venv'
subprocess.run([sys.executable, '-m', 'venv', str(ambiente)], check=True)
python = ambiente / 'Scripts' / 'python.exe'
subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(raiz/'requirements.txt')], check=True)
subprocess.run([str(python), '-c', 'import sys,django,fastapi,pydantic,uvicorn; print(sys.version); print("Django",django.get_version(),"FastAPI",fastapi.__version__,"Pydantic",pydantic.__version__,"Uvicorn",uvicorn.__version__)'], check=True)
print('Ambiente pronto. Execute as tarefas 2 e 3 em terminais separados.')
