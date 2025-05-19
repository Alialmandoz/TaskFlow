# TaskFlowProject/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv # Para cargar variables de entorno desde .env en desarrollo local

# Carga las variables del archivo .env si existe (para desarrollo local)
# load_dotenv() no fallará si el archivo .env no existe (como en producción en PythonAnywhere)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURACIÓN DE PRODUCCIÓN Y DESARROLLO ---

# SECRET_KEY: Se leerá de una variable de entorno en PythonAnywhere ('DJANGO_SECRET_KEY').
# Para desarrollo local, si no está la variable de entorno, usa la clave actual como fallback.
# ¡¡ASEGÚRATE DE CONFIGURAR 'DJANGO_SECRET_KEY' COMO VARIABLE DE ENTORNO EN PYTHONANYWHERE!!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-fok@f_mk=_!+i3%fj=dcv#y)#o)tx1l=g6z$_ziiv%ig&gn_(d' # Tu clave actual como fallback
)

# GOOGLE_API_KEY: Se lee de una variable de entorno.
# ¡¡ASEGÚRATE DE CONFIGURAR 'GOOGLE_API_KEY' COMO VARIABLE DE ENTORNO EN PYTHONANYWHERE!!
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# DEBUG: Para producción, esto DEBE ser False.
DEBUG = False

# ALLOWED_HOSTS: Configurado para tu dominio de PythonAnywhere.
# Si luego añades un dominio personalizado, también deberás añadirlo aquí.
ALLOWED_HOSTS = ['alialmandoz.pythonanywhere.com']
# Si necesitas añadir más hosts en el futuro:
# ALLOWED_HOSTS = ['alialmandoz.pythonanywhere.com', 'www.tu_dominio_personalizado.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'tasks.apps.TasksConfig',
    'accounting.apps.AccountingConfig',
    'dashboard.apps.DashboardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TaskFlowProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Si tienes plantillas a nivel de proyecto
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TaskFlowProject.wsgi.application'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es' # Asumiendo que prefieres español
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_production' # Directorio para collectstatic

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Seguridad Adicional para Producción (cuando DEBUG = False y HTTPS está configurado) ---
# Descomenta y ajusta estas configuraciones una vez que HTTPS esté funcionando en PythonAnywhere.
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = False # Empieza con False, cámbialo a True después de confirmar que HTTPS funciona
# SECURE_HSTS_SECONDS = 2592000  # Ejemplo: 30 días
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'