# Configuração exclusiva para demonstração local.
SECRET_KEY = 'apenas-laboratorio-local'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
ROOT_URLCONF = 'config.urls'
INSTALLED_APPS = []
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]
