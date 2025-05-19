# Contenido del Proyecto: TaskFlow

**Generado el:** 2025-05-18 22:35:58

## Estructura del Proyecto

```text
TaskFlow
├── TaskFlowProject
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── templates
│   │   └── registration
│   │       ├── logged_out.html
│   │       ├── login.html
│   │       ├── password_change_done.html
│   │       ├── password_change_form.html
│   │       ├── password_reset_complete.html
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_done.html
│   │       └── password_reset_form.html
│   ├── urls.py
│   └── wsgi.py
├── accounting
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_transaction_original_instruction_alter_category_name.py
│   │   └── __init__.py
│   ├── models.py
│   ├── services.py
│   ├── templates
│   │   └── accounting
│   │       ├── transaction_form.html
│   │       └── transaction_list.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── dashboard
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   │   └── dashboard
│   │       └── js
│   │           └── dashboard_logic.js
│   ├── templates
│   │   └── dashboard
│   │       └── dashboard.html
│   ├── tests.py
│   └── views.py
├── manage.py
├── requirements.txt
├── start.bat
├── tasks
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_project_original_instruction_and_more.py
│   │   └── __init__.py
│   ├── models.py
│   ├── services.py
│   ├── templates
│   │   └── tasks
│   │       ├── base.html
│   │       ├── project_detail.html
│   │       ├── project_form.html
│   │       ├── project_list.html
│   │       └── task_form.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── ui.psd
```

---

## Archivo: `TaskFlowProject/__init__.py`

```python

```

---

## Archivo: `TaskFlowProject/asgi.py`

```python
"""
ASGI config for TaskFlowProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskFlowProject.settings')

application = get_asgi_application()

```

---

## Archivo: `TaskFlowProject/settings.py`

```python
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

# --- CONFIGURACIÓN DE AUTENTICACIÓN ---
LOGIN_URL = '/accounts/login/'  # La URL donde los usuarios serán redirigidos para iniciar sesión.
                              # Coincide con la que Django usa por defecto y la que acabamos de añadir.

LOGIN_REDIRECT_URL = '/'      # A dónde ir después de un login exitoso.
                              # '/' apuntará a tu dashboard_view.
                              # Puedes cambiarlo a 'dashboard' si prefieres usar el nombre de la URL.

LOGOUT_REDIRECT_URL = '/'     # A dónde ir después de un logout exitoso (opcional, pero bueno tenerlo).
# --- FIN CONFIGURACIÓN DE AUTENTICACIÓN ---


# Configuración de Email para Desarrollo (imprime en consola)
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else:
    # Para producción, necesitarás configurar un backend de email real (SMTP)
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_HOST = 'smtp.example.com'
    # EMAIL_PORT = 587
    # EMAIL_USE_TLS = True
    # EMAIL_HOST_USER = 'tu_email@example.com'
    # EMAIL_HOST_PASSWORD = 'tu_password_de_email_o_app_password'
    # DEFAULT_FROM_EMAIL = 'noreply@taskflowapp.com'
```

---

## Archivo: `TaskFlowProject/templates/registration/logged_out.html`

```html
{# TaskFlow/templates/registration/logged_out.html #}
{% extends "tasks/base.html" %}

{% block title %}Sesión Cerrada - TaskFlow{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-body text-center p-4">
                    <h2>Has cerrado sesión.</h2>
                    <p>¡Gracias por usar TaskFlow! Esperamos verte pronto.</p>
                    <a href="{% url 'login' %}" class="btn btn-primary mt-3">Iniciar Sesión de Nuevo</a>
                    <a href="{% url 'dashboard' %}" class="btn btn-outline-secondary mt-3 ms-2">Ir al Dashboard (si es público)</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Archivo: `TaskFlowProject/templates/registration/login.html`

```html
{# TaskFlow/templates/registration/login.html #}
{% extends "tasks/base.html" %} {# O la plantilla base de tu proyecto si tienes una diferente #}
{% load crispy_forms_tags %}

{% block title %}Iniciar Sesión - TaskFlow{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h2 class="card-title mb-0 text-center">Iniciar Sesión en TaskFlow</h2>
                </div>
                <div class="card-body p-4">
                    {% if form.errors %}
                        <div class="alert alert-danger" role="alert">
                            Tu nombre de usuario y contraseña no coinciden. Por favor, inténtalo de nuevo.
                        </div>
                    {% endif %}

                    {% if next %}
                        {% if user.is_authenticated %}
                        <div class="alert alert-warning" role="alert">
                            Tu cuenta no tiene acceso a esta página. Para proceder,
                            por favor inicia sesión con una cuenta que tenga acceso.
                        </div>
                        {% else %}
                        <div class="alert alert-info" role="alert">
                            Por favor, inicia sesión para ver esta página.
                        </div>
                        {% endif %}
                    {% endif %}

                    <form method="post" action="{% url 'login' %}">
                        {% csrf_token %}
                        {{ form|crispy }}
                        <input type="hidden" name="next" value="{{ next|default:'/' }}"> {# Redirige a 'next' o a la raíz por defecto #}
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-block mt-3">Iniciar Sesión</button>
                        </div>
                    </form>
                    <hr>
                    <div class="text-center">
                        {# Descomenta estas líneas cuando implementes estas funcionalidades #}
                        {# <p><a href="{% url 'password_reset' %}">¿Olvidaste tu contraseña?</a></p> #}
                        {# <p>¿No tienes una cuenta? <a href="{% url 'signup' %}">Regístrate</a></p> #}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Archivo: `TaskFlowProject/templates/registration/password_change_done.html`

```html
{# TaskFlow/templates/registration/password_change_done.html #}
{% extends "tasks/base.html" %}

{% block title %}Contraseña Cambiada - TaskFlow{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-body text-center p-4">
                    <h2>¡Contraseña Cambiada con Éxito!</h2>
                    <p>Tu contraseña ha sido actualizada.</p>
                    <a href="{% url 'dashboard' %}" class="btn btn-primary mt-3">Volver al Dashboard</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Archivo: `TaskFlowProject/templates/registration/password_change_form.html`

```html
{# TaskFlow/templates/registration/password_change_form.html #}
{% extends "tasks/base.html" %}
{% load crispy_forms_tags %}

{% block title %}Cambiar Contraseña - TaskFlow{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h2 class="card-title mb-0 text-center">Cambiar Contraseña</h2>
                </div>
                <div class="card-body p-4">
                    <p>Por favor, introduce tu contraseña antigua, y luego tu nueva contraseña dos veces para que podamos verificar que la has escrito correctamente.</p>
                    <form method="post">
                        {% csrf_token %}
                        {{ form|crispy }}
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-block mt-3">Cambiar mi Contraseña</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Archivo: `TaskFlowProject/templates/registration/password_reset_complete.html`

```html
{# TaskFlow/templates/registration/password_reset_complete.html #}
{% extends "tasks/base.html" %}

{% block title %}Contraseña Restablecida - TaskFlow{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-body text-center p-4">
                    <h2>¡Contraseña Restablecida con Éxito!</h2>
                    <p>Tu contraseña ha sido establecida. Ahora puedes iniciar sesión con tu nueva contraseña.</p>
                    <a href="{% url 'login' %}" class="btn btn-primary mt-3">Iniciar Sesión</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Archivo: `TaskFlowProject/templates/registration/password_reset_confirm.html`

```html
{# TaskFlow/templates/registration/password_reset_confirm.html #}
{% extends "tasks/base.html" %}
{% load crispy_forms_tags %}

{% block title %}Establecer Nueva Contraseña - TaskFlow{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h2 class="card-title mb-0 text-center">Establecer Nueva Contraseña</h2>
                </div>
                <div class="card-body p-4">
                    {% if validlink %}
                        <p>Por favor, introduce tu nueva contraseña dos veces para que podamos verificar que la has escrito correctamente.</p>
                        <form method="post">
                            {% csrf_token %}
                            {{ form|crispy }}
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary btn-block mt-3">Establecer Nueva Contraseña</button>
                            </div>
                        </form>
                    {% else %}
                        <div class="alert alert-danger" role="alert">
                            El enlace para restablecer la contraseña no es válido, posiblemente porque ya ha sido utilizado o ha expirado.
                            Por favor, solicita un nuevo restablecimiento de contraseña.
                        </div>
                        <div class="text-center">
                             <a href="{% url 'password_reset' %}" class="btn btn-warning mt-2">Solicitar Nuevo Restablecimiento</a>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Archivo: `TaskFlowProject/templates/registration/password_reset_done.html`

```html
{# TaskFlow/templates/registration/password_reset_done.html #}
{% extends "tasks/base.html" %}

{% block title %}Enlace Enviado - TaskFlow{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-body text-center p-4">
                    <h2>Enlace de Restablecimiento Enviado</h2>
                    <p>Te hemos enviado un correo electrónico con las instrucciones para restablecer tu contraseña, si existe una cuenta con el correo que ingresaste. Deberías recibirlo en breve.</p>
                    <p>Si no recibes un correo, por favor asegúrate de que has introducido la dirección con la que te registraste y revisa tu carpeta de spam.</p>
                    <a href="{% url 'login' %}" class="btn btn-outline-secondary mt-3">Volver a Iniciar Sesión</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Archivo: `TaskFlowProject/templates/registration/password_reset_form.html`

```html
{# TaskFlow/templates/registration/password_reset_form.html #}
{% extends "tasks/base.html" %}
{% load crispy_forms_tags %}

{% block title %}Restablecer Contraseña - TaskFlow{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h2 class="card-title mb-0 text-center">Restablecer Contraseña</h2>
                </div>
                <div class="card-body p-4">
                    <p>¿Olvidaste tu contraseña? Introduce tu dirección de correo electrónico a continuación y te enviaremos instrucciones para establecer una nueva.</p>
                    <form method="post">
                        {% csrf_token %}
                        {{ form|crispy }}
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-block mt-3">Enviar Enlace de Restablecimiento</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Archivo: `TaskFlowProject/urls.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\TaskFlowProject\urls.py

from django.contrib import admin
from django.urls import path, include # Asegúrate de que include esté importado
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_views.dashboard_view, name='dashboard'),
    path('tasks/', include('tasks.urls')),
    path('accounting/', include('accounting.urls')),

    # --- AÑADIDO: URLs de autenticación de Django ---
    path('accounts/', include('django.contrib.auth.urls')),
    # ----------------------------------------------
]
```

---

## Archivo: `TaskFlowProject/wsgi.py`

```python
"""
WSGI config for TaskFlowProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskFlowProject.settings')

application = get_wsgi_application()

```

---

## Archivo: `accounting/__init__.py`

```python

```

---

## Archivo: `accounting/admin.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\admin.py

from django.contrib import admin
from .models import Category, Transaction
from tasks.models import Project # Para filtrar en formfield_for_foreignkey

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if not request.user.is_superuser and not hasattr(obj, 'user'):
                obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'transaction_date', 'category', 'project', 'user', 'type', 'original_instruction') # <-- AÑADIDO a list_display
    list_filter = ('transaction_date', 'user', 'category', 'project', 'type')
    search_fields = ('description', 'notes', 'user__username', 'project__name', 'category__name', 'original_instruction') # <-- AÑADIDO a search_fields
    list_editable = ('amount', 'category')
    date_hierarchy = 'transaction_date'
    fieldsets = (
        (None, {
            'fields': ('user', 'description', 'amount', 'type', 'transaction_date')
        }),
        ('Asociaciones', {
            'fields': ('category', 'project')
        }),
        ('Notas Adicionales', {
            # --- MODIFICADO: Añadir original_instruction aquí ---
            'fields': ('notes', 'original_instruction'),
            'classes': ('collapse',)
        }),
    )
    # --- AÑADIDO: Hacer original_instruction readonly en el admin si se desea ---
    readonly_fields = ('original_instruction',)


    def save_model(self, request, obj, form, change):
        if not obj.pk:
             if not request.user.is_superuser and not hasattr(obj, 'user'): # Si no es superuser y el usuario no está seteado
                obj.user = request.user # Asignar el usuario actual
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "category":
                kwargs["queryset"] = Category.objects.filter(user=request.user)
            if db_field.name == "project":
                kwargs["queryset"] = Project.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
```

---

## Archivo: `accounting/apps.py`

```python
from django.apps import AppConfig


class AccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting'

```

---

## Archivo: `accounting/forms.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\forms.py

from django import forms
from .models import Transaction, Category # Importamos Category para el filtro
from tasks.models import Project

class TransactionForm(forms.ModelForm):
    """
    Formulario para crear y actualizar Transacciones (gastos).
    (Sin cambios respecto a la versión anterior)
    """
    transaction_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de la Transacción"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        label="Categoría"
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.none(),
        required=False,
        label="Proyecto Asociado (Opcional)"
    )

    class Meta:
        model = Transaction
        fields = [
            'description',
            'amount',
            'transaction_date',
            'type',
            'category',
            'project',
            'notes'
            # 'original_instruction' no se incluye aquí, se maneja programáticamente
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'description': forms.TextInput(attrs={'placeholder': 'Ej: Almuerzo con cliente'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Ej: 25.50'}),
        }
        labels = {
            'description': 'Descripción del Gasto',
            'amount': 'Monto ($)',
            'type': 'Tipo de Transacción',
            'notes': 'Notas Adicionales',
        }
        help_texts = {
            'type': 'Actualmente solo se registran gastos.',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')
            self.fields['project'].queryset = Project.objects.filter(user=user).order_by('name')
        else:
            self.fields['category'].queryset = Category.objects.none()
            self.fields['project'].queryset = Project.objects.none()
        self.fields['type'].initial = 'expense'

# --- AÑADIDO: Formulario para filtrar transacciones ---
class TransactionFilterForm(forms.Form):
    """
    Formulario para filtrar la lista de transacciones.
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(), # Se llenará dinámicamente en la vista
        required=False, # Permitir no filtrar por categoría (mostrar todas)
        label="Filtrar por Categoría",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}) # Estilo Bootstrap
    )
    # Podríamos añadir más filtros aquí en el futuro (ej. rango de fechas, proyecto)
    # start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}))
    # end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}))

    def __init__(self, *args, **kwargs):
        # El usuario es necesario para poblar el queryset de categorías
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')
        else:
            # Si no hay usuario (ej. admin global), podríamos mostrar todas o ninguna
            # Para un usuario normal, esto no debería pasar si la vista está protegida.
            self.fields['category'].queryset = Category.objects.none()
# --- FIN AÑADIDO ---
```

---

## Archivo: `accounting/migrations/0001_initial.py`

```python
# Generated by Django 5.2 on 2025-05-10 15:41

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('user', models.ForeignKey(help_text='Usuario al que pertenece esta categoría', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Descripción del gasto.', max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Monto del gasto.', max_digits=10)),
                ('transaction_date', models.DateField(default=django.utils.timezone.now, help_text='Fecha en que se realizó el gasto.')),
                ('type', models.CharField(choices=[('expense', 'Gasto')], default='expense', help_text='Tipo de transacción (actualmente solo Gasto).', max_length=10)),
                ('notes', models.TextField(blank=True, help_text='Notas adicionales sobre el gasto (opcional).', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, help_text='Categoría del gasto.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.category')),
                ('project', models.ForeignKey(blank=True, help_text='Proyecto de TaskFlow al que está asociado este gasto (opcional).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.project')),
                ('user', models.ForeignKey(help_text='Usuario que registró el gasto.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transacción',
                'verbose_name_plural': 'Transacciones',
                'ordering': ['-transaction_date', '-created_at'],
            },
        ),
    ]

```

---

## Archivo: `accounting/migrations/0002_transaction_original_instruction_alter_category_name.py`

```python
# Generated by Django 5.2 on 2025-05-13 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='original_instruction',
            field=models.TextField(blank=True, help_text='La instrucción original del usuario si fue creado vía IA.', null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]

```

---

## Archivo: `accounting/migrations/__init__.py`

```python

```

---

## Archivo: `accounting/models.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\models.py

from django.db import models
from django.contrib.auth.models import User
from tasks.models import Project # Para asociar a un proyecto de la app 'tasks'
from django.utils import timezone

class Category(models.Model):
    """
    Representa una categoría para las transacciones (gastos/ingresos).
    """
    name = models.CharField(max_length=100) # unique=True se maneja con unique_together
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario al que pertenece esta categoría")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        unique_together = ('name', 'user') # Nombre de categoría único por usuario

    def __str__(self):
        return f"{self.name} (Usuario: {self.user.username})"

class Transaction(models.Model):
    """
    Representa una transacción financiera, principalmente un gasto.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('expense', 'Gasto'),
        # ('income', 'Ingreso'),
    ]

    description = models.CharField(max_length=255, help_text="Descripción del gasto.")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto del gasto.")
    transaction_date = models.DateField(default=timezone.now, help_text="Fecha en que se realizó el gasto.")
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        default='expense',
        help_text="Tipo de transacción (actualmente solo Gasto)."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Categoría del gasto."
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Proyecto de TaskFlow al que está asociado este gasto (opcional)."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Usuario que registró el gasto."
    )
    notes = models.TextField(blank=True, null=True, help_text="Notas adicionales sobre el gasto (opcional).")
    # --- AÑADIDO ---
    original_instruction = models.TextField(
        null=True,
        blank=True,
        help_text="La instrucción original del usuario si fue creado vía IA."
    )
    # --- FIN AÑADIDO ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-transaction_date', '-created_at']

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.user.username})"
```

---

## Archivo: `accounting/services.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\services.py

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, date as python_date
from decimal import Decimal, InvalidOperation

from .models import Transaction, Category # Category es necesario para crear/buscar
from tasks.models import Project

# --- MODIFICADO: create_transaction_from_data para manejar ID de categoría o creación de nueva categoría ---
def create_transaction_from_data(
    user: User,
    description: str,
    amount: float | int | str,
    transaction_date_str: str | None,
    # Nuevos parámetros para categoría:
    selected_category_id: int | None,
    create_category_with_name: str | None,
    # project_name sigue igual
    project_name: str | None,
    original_instruction: str = None
) -> Transaction:
    """
    Crea y guarda una nueva transacción (gasto).
    Asigna una categoría existente por ID, o crea y asigna una nueva categoría por nombre.
    """
    if not isinstance(user, User):
        raise TypeError("Se requiere un objeto User válido.")
    if not description:
        raise ValueError("La descripción de la transacción no puede estar vacía.")
    if amount is None:
         raise ValueError("El monto de la transacción no puede estar vacío.")

    try:
        decimal_amount = Decimal(str(amount))
        if not decimal_amount.is_finite():
             raise ValueError("El monto proporcionado no es un número finito válido.")
    except (InvalidOperation, ValueError):
        raise ValueError(f"El monto '{amount}' no es un valor numérico válido.")

    print(f"DEBUG: [Accounting Service] Intentando procesar fecha. transaction_date_str: '{transaction_date_str}'")
    parsed_date_obj: python_date
    if transaction_date_str and transaction_date_str.strip():
        try:
            dt_naive = datetime.strptime(transaction_date_str, "%Y-%m-%d")
            parsed_date_obj = dt_naive.date()
            print(f"DEBUG: [Accounting Service] Fecha parseada de string: {parsed_date_obj}")
        except ValueError as e:
            print(f"ERROR: [Accounting Service] Falló strptime para '{transaction_date_str}': {e}. Usando fecha actual.")
            parsed_date_obj = timezone.localdate()
    else:
        print(f"DEBUG: [Accounting Service] transaction_date_str vacío/None. Usando fecha actual.")
        parsed_date_obj = timezone.localdate()
    print(f"DEBUG: [Accounting Service] Fecha a usar para la transacción: {parsed_date_obj}")

    category_obj = None
    # --- Lógica de Categoría Modificada ---
    if selected_category_id:
        try:
            category_obj = Category.objects.get(pk=selected_category_id, user=user)
            print(f"DEBUG: [Accounting Service] Categoría seleccionada por ID: {category_obj.name}")
        except Category.DoesNotExist:
            print(f"WARN: [Accounting Service] Categoría con ID '{selected_category_id}' no encontrada para el usuario {user.username}. Se ignorará.")
            # Podríamos lanzar un error aquí si el ID debería ser siempre válido.
    elif create_category_with_name and create_category_with_name.strip():
        category_name_cleaned = create_category_with_name.strip()
        # Intentar obtenerla por si ya existe (case-insensitive) para evitar duplicados exactos
        category_obj, created = Category.objects.get_or_create(
            user=user,
            name__iexact=category_name_cleaned, # Buscar ignorando mayúsculas/minúsculas
            defaults={'name': category_name_cleaned, 'user': user} # Asegurar el nombre correcto al crear
        )
        if created:
            print(f"INFO: [Accounting Service] Nueva categoría '{category_obj.name}' creada para el usuario {user.username}.")
        else:
            print(f"DEBUG: [Accounting Service] Categoría existente '{category_obj.name}' encontrada y usada para el nombre '{category_name_cleaned}'.")
    else:
        print(f"DEBUG: [Accounting Service] No se seleccionó ni se creó una categoría.")
    # --- Fin Lógica de Categoría Modificada ---

    project_obj = None
    if project_name:
        try:
            project_obj = Project.objects.get(user=user, name__iexact=project_name)
            print(f"DEBUG: [Accounting Service] Proyecto encontrado: {project_obj.name}")
        except Project.DoesNotExist:
            print(f"WARN: [Accounting Service] Proyecto '{project_name}' no encontrado. Se registrará sin proyecto.")

    transaction = Transaction(
        user=user,
        description=description,
        amount=decimal_amount,
        transaction_date=parsed_date_obj,
        category=category_obj, # Puede ser None, o la seleccionada/creada
        project=project_obj,
        type='expense',
        original_instruction=original_instruction
    )
    transaction.save()

    print(f"INFO: [Accounting Service] Transacción creada ID: {transaction.id}. Fecha: {transaction.transaction_date}. Categoría: {transaction.category.name if transaction.category else 'N/A'}")
    return transaction
# --- FIN MODIFICADO ---
```

---

## Archivo: `accounting/templates/accounting/transaction_form.html`

```html
{# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\templates\accounting\transaction_form.html #}
{% extends "tasks/base.html" %}
{% load crispy_forms_tags %}

{% block title %}{{ page_title|default:"Gestionar Transacción" }} - TaskFlow Contabilidad{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>{{ page_title|default:"Gestionar Transacción" }}</h2>
    <hr>

    <form method="post" novalidate>
        {% csrf_token %}
        
        {# Esta es la única directiva que renderiza el cuerpo del formulario. #}
        {{ form|crispy }} 

        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Guardar Transacción</button>
            <a href="{% url 'tasks:project_list' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}

{% block javascript %}
{{ super }}
{# Espacio para JavaScript específico de esta página si fuera necesario más adelante. #}
{# 
<script>
    // Ejemplo:
    // document.addEventListener('DOMContentLoaded', function() {
    //     var dateInput = document.querySelector('input[type="date"]');
    //     if (dateInput && dateInput.type !== 'date') { 
    //         dateInput.setAttribute('placeholder', 'AAAA-MM-DD');
    //     }
    // });
</script>
#}
{% endblock %}
```

---

## Archivo: `accounting/templates/accounting/transaction_list.html`

```html
{# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\templates\accounting\transaction_list.html #}
{% extends "tasks/base.html" %}
{% load crispy_forms_tags %}
{% load l10n %}

{% block title %}{{ page_title|default:"Mis Gastos" }} - TaskFlow Contabilidad{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>{{ page_title|default:"Mis Gastos" }}</h2>
        <a href="{% url 'accounting:transaction_create' %}" class="btn btn-primary">
            {# <i class="fas fa-plus me-1"></i> #} Registrar Nuevo Gasto
        </a>
    </div>
    <hr>

    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">Filtrar Gastos</h5>
            <form method="get" class="row gx-3 gy-2 align-items-center">
                <div class="col-sm-auto">
                     {{ filter_form.category.label_tag }}
                     {{ filter_form.category }}
                </div>
                <!--
                Ejemplo si tuvieras más filtros:
                <div class="col-sm-auto">
                     {{ filter_form.start_date.label_tag }}
                     {{ filter_form.start_date }}
                </div>
                <div class="col-sm-auto">
                     {{ filter_form.end_date.label_tag }}
                     {{ filter_form.end_date }}
                </div>
                -->
                <div class="col-sm-auto">
                    <button type="submit" class="btn btn-info btn-sm mt-4">Aplicar Filtro</button>
                    <a href="{% url 'accounting:transaction_list' %}" class="btn btn-secondary btn-sm mt-4 ms-2">Limpiar</a>
                </div>
            </form>
        </div>
    </div>

    {% if page_obj.object_list %}
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th scope="col">Fecha</th>
                        <th scope="col">Descripción</th>
                        <th scope="col" class="text-end">Monto</th>
                        <th scope="col">Categoría</th>
                        <th scope="col">Proyecto</th>
                        <!-- <th scope="col">Acciones</th> --> {# Columna de acciones comentada por ahora #}
                    </tr>
                </thead>
                <tbody>
                    {% for transaction in page_obj.object_list %}
                    <tr>
                        <td>{{ transaction.transaction_date|date:"d M Y" }}</td>
                        <td>
                            {{ transaction.description }}
                            {% if transaction.original_instruction %}
                                <small class="d-block text-muted" title="Instrucción original IA: {{ transaction.original_instruction }}">
                                    {# <i class="fas fa-robot fa-xs"></i> #} Creado por IA
                                </small>
                            {% endif %}
                        </td>
                        <td class="text-end">{{ transaction.amount|floatformat:2 }} €</td>
                        <td>{{ transaction.category.name|default:"-" }}</td>
                        <td>{{ transaction.project.name|default:"-" }}</td>
                        <!--
                        <td>
                            <a href="#" class="btn btn-sm btn-outline-secondary disabled">Editar</a>
                        </td>
                        -->
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        {% if page_obj.has_other_pages %}
            <nav aria-label="Navegación de transacciones">
                <ul class="pagination justify-content-center">
                    {% if page_obj.has_previous %}
                        <li class="page-item">
                            <a class="page-link" href="?page=1{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">&laquo; Primera</a>
                        </li>
                        <li class="page-item">
                            <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">Anterior</a>
                        </li>
                    {% else %}
                        <li class="page-item disabled"><span class="page-link">&laquo; Primera</span></li>
                        <li class="page-item disabled"><span class="page-link">Anterior</span></li>
                    {% endif %}

                    {% for num in page_obj.paginator.page_range %}
                        {% if page_obj.number == num %}
                            <li class="page-item active" aria-current="page"><span class="page-link">{{ num }}</span></li>
                        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                            <li class="page-item"><a class="page-link" href="?page={{ num }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">{{ num }}</a></li>
                        {% endif %}
                    {% endfor %}

                    {% if page_obj.has_next %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">Siguiente</a>
                        </li>
                        <li class="page-item">
                            <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">Última &raquo;</a>
                        </li>
                    {% else %}
                        <li class="page-item disabled"><span class="page-link">Siguiente</span></li>
                        <li class="page-item disabled"><span class="page-link">Última &raquo;</span></li>
                    {% endif %}
                </ul>
            </nav>
        {% endif %}

    {% else %}
        <div class="alert alert-info" role="alert">
            Aún no tienes gastos registrados que coincidan con los filtros seleccionados.
            <a href="{% url 'accounting:transaction_create' %}" class="alert-link">¿Quieres registrar uno nuevo?</a>
        </div>
    {% endif %}
</div>

<!--
Si no usas FontAwesome globalmente, necesitarías añadir el CSS en base.html o aquí.
Ejemplo de CDN para FontAwesome (añadir a base.html si se usa en más sitios):
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
He comentado los iconos <i> por ahora para evitar errores si no está configurado.
-->
{% endblock %}
```

---

## Archivo: `accounting/tests.py`

```python
from django.test import TestCase

# Create your tests here.

```

---

## Archivo: `accounting/urls.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\urls.py

from django.urls import path
from . import views # Importamos las vistas de esta app

app_name = 'accounting' # Define un namespace para estas URLs

urlpatterns = [
    # URL para añadir una nueva transacción
    path('transaction/add/', views.transaction_create, name='transaction_create'),

    # --- AÑADIDO: URL para listar transacciones ---
    path('transactions/', views.transaction_list, name='transaction_list'),
    # --- FIN AÑADIDO ---
]
```

---

## Archivo: `accounting/views.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# --- MODIFICADO: Importar el nuevo formulario de filtro ---
from .forms import TransactionForm, TransactionFilterForm
from .models import Transaction, Category # Category para el filtro
# --- FIN MODIFICADO ---
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Para paginación

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            # --- MODIFICADO: Redirigir a la nueva lista de transacciones ---
            return redirect(reverse_lazy('accounting:transaction_list'))
    else:
        form = TransactionForm(user=request.user)
    context = {
        'form': form,
        'page_title': 'Registrar Nuevo Gasto'
    }
    return render(request, 'accounting/transaction_form.html', context)

# --- AÑADIDO: Vista para listar transacciones ---
@login_required
def transaction_list(request):
    """
    Muestra una lista paginada de transacciones (gastos) para el usuario actual,
    con la opción de filtrar por categoría.
    """
    transactions_qs = Transaction.objects.filter(user=request.user, type='expense').select_related(
        'category', 'project' # Optimizar para acceso en plantilla
    ).order_by('-transaction_date', '-created_at')

    # Inicializar el formulario de filtro (pasando el usuario para poblar categorías)
    filter_form = TransactionFilterForm(request.GET or None, user=request.user)

    if filter_form.is_valid():
        category_filter = filter_form.cleaned_data.get('category')
        if category_filter:
            transactions_qs = transactions_qs.filter(category=category_filter)
        # Aquí se podrían añadir más filtros si el formulario los tuviera
        # start_date = filter_form.cleaned_data.get('start_date')
        # end_date = filter_form.cleaned_data.get('end_date')
        # if start_date:
        #     transactions_qs = transactions_qs.filter(transaction_date__gte=start_date)
        # if end_date:
        #     transactions_qs = transactions_qs.filter(transaction_date__lte=end_date)

    # Paginación
    paginator = Paginator(transactions_qs, 10) # Mostrar 10 transacciones por página
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Si page no es un entero, entregar la primera página.
        page_obj = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango (ej. 9999), entregar la última página de resultados.
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj, # Objeto de página para la plantilla (contiene las transacciones de la página actual)
        'filter_form': filter_form,
        'page_title': 'Mis Gastos Registrados'
    }
    return render(request, 'accounting/transaction_list.html', context)
# --- FIN AÑADIDO ---
```

---

## Archivo: `dashboard/__init__.py`

```python

```

---

## Archivo: `dashboard/admin.py`

```python
from django.contrib import admin

# Register your models here.

```

---

## Archivo: `dashboard/apps.py`

```python
from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

```

---

## Archivo: `dashboard/migrations/__init__.py`

```python

```

---

## Archivo: `dashboard/models.py`

```python
from django.db import models

# Create your models here.

```

---

## Archivo: `dashboard/static/dashboard/js/dashboard_logic.js`

```javascript
// dashboard/static/dashboard/js/dashboard_logic.js

// Esperar a que el DOM esté completamente cargado para asegurar que window.AI_COMMAND_HANDLER_URL esté disponible
// y que los elementos del formulario existan.
document.addEventListener('DOMContentLoaded', function() {

    // Elementos del DOM
    const aiCommandForm = document.getElementById('aiCommandForm');
    const instructionTextarea = document.getElementById('instruction');
    const responseArea = document.getElementById('responseArea');
    
    // El input del token CSRF se espera que esté en el <form> dentro del HTML.
    // Lo obtendremos directamente cuando lo necesitemos.

    // Obtener la URL del handler de la variable global 'window' definida en el HTML
    const aiCommandHandlerUrl = window.AI_COMMAND_HANDLER_URL;

    // Verificar si los elementos cruciales y la URL están disponibles
    if (!aiCommandForm || !instructionTextarea || !responseArea || !aiCommandHandlerUrl) {
        console.error('Error crítico: Faltan elementos esenciales del DOM (formulario, textarea, área de respuesta) o la URL del AI Handler no está definida en window.AI_COMMAND_HANDLER_URL.');
        if (responseArea) { // Intentar mostrar error en el área de respuesta si existe
             responseArea.innerHTML = '<p class="error">Error de inicialización del interfaz de IA. Verifique la consola.</p>';
        }
        return; // Detener la ejecución del script si falta algo crucial
    }

    // Listener para el formulario principal de la consola de IA
    aiCommandForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevenir el envío tradicional del formulario
        const instruction = instructionTextarea.value.trim();
        if (!instruction) return; // No hacer nada si la instrucción está vacía

        responseArea.innerHTML = '<p class="loading">Procesando tu instrucción...</p>';
        instructionTextarea.value = ''; // Limpiar el textarea

        // Obtener el token CSRF del input oculto en el formulario
        const csrfTokenInput = aiCommandForm.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfTokenInput) {
            console.error("Error crítico: Input de token CSRF no encontrado en el formulario.");
            responseArea.innerHTML = '<p class="error">Error de configuración: Falta token CSRF.</p>';
            return;
        }
        const currentCsrfToken = csrfTokenInput.value;

        try {
            const response = await fetch(aiCommandHandlerUrl, { // Usar la variable obtenida de window
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': currentCsrfToken
                },
                body: JSON.stringify({ instruction: instruction })
            });

            const data = await response.json(); // Asumimos que la respuesta siempre será JSON o fallará el parseo

            if (response.ok || data.error) { // data.error para errores controlados por el backend con status 200 o 400
                if (data.action_needed === 'confirm_expense') {
                    displayConfirmationUI(data);
                } else if (data.error) {
                     responseArea.innerHTML = `<p class="error"><strong>Error:</strong> ${data.error}</p>`;
                } else { // Cualquier otra respuesta exitosa sin acción específica o error
                    handleSuccessfulResponse(data);
                }
            } else { // Errores de red o HTTP no OK que no devolvieron JSON con 'error'
                responseArea.innerHTML = `<p class="error"><strong>Error ${response.status}:</strong> ${data.error || 'Ocurrió un error inesperado en el servidor.'}</p>`;
            }
        } catch (error) { // Captura errores del fetch en sí o del response.json()
            console.error('Error en la solicitud inicial AI:', error);
            responseArea.innerHTML = `<p class="error"><strong>Error de conexión o script:</strong> ${error.message}</p>`;
        }
    });

    // Función para mostrar la UI de confirmación de gastos
    function displayConfirmationUI(data) {
        responseArea.innerHTML = ''; // Limpiar área de respuesta

        const messageP = document.createElement('p');
        messageP.textContent = data.message || 'Por favor, confirma los detalles:';
        responseArea.appendChild(messageP);

        const detailsContainer = document.createElement('div');
        detailsContainer.style.padding = '10px';
        detailsContainer.style.border = '1px solid #ccc';
        detailsContainer.style.borderRadius = '4px';
        detailsContainer.style.backgroundColor = '#f8f9fa';
        detailsContainer.style.marginBottom = '15px';

        // Mostrar datos extraídos (descripción, monto, fecha, instrucción original)
        for (const [key, value] of Object.entries(data.extracted_data)) {
            if (key !== 'category_name_guess' && value !== null && value !== undefined) {
                const detailP = document.createElement('p');
                detailP.style.margin = '5px 0';
                const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                detailP.innerHTML = `<strong>${label}:</strong> ${value}`;
                detailsContainer.appendChild(detailP);
            }
        }

        // Sección para Categorías
        const categorySection = document.createElement('div');
        categorySection.classList.add('mb-3');

        const categoryLabel = document.createElement('label');
        categoryLabel.htmlFor = 'category_select_dropdown';
        categoryLabel.textContent = 'Categoría del Gasto:';
        categoryLabel.classList.add('form-label');
        categorySection.appendChild(categoryLabel);

        const categorySelect = document.createElement('select');
        categorySelect.id = 'category_select_dropdown';
        // console.log("Elemento categorySelect creado con ID:", categorySelect.id, categorySelect);
        categorySelect.classList.add('form-select', 'form-select-sm', 'mb-2');

        const defaultOption = document.createElement('option');
        defaultOption.value = ""; // Valor vacío para "ninguna seleccionada"
        defaultOption.textContent = "--- Seleccionar Categoría Existente ---";
        categorySelect.appendChild(defaultOption);

        let geminiGuessExistsInUserCategories = false;
        if (data.user_categories && data.user_categories.length > 0) {
            data.user_categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.name;
                if (data.extracted_data.category_name_guess &&
                    cat.name.toLowerCase() === data.extracted_data.category_name_guess.toLowerCase()) {
                    option.selected = true;
                    geminiGuessExistsInUserCategories = true;
                }
                categorySelect.appendChild(option);
            });
        } else {
            const noCatOption = document.createElement('option');
            noCatOption.value = "";
            noCatOption.textContent = "No hay categorías creadas";
            noCatOption.disabled = true;
            categorySelect.appendChild(noCatOption);
        }
        categorySection.appendChild(categorySelect);

        const newCategoryLabel = document.createElement('label');
        newCategoryLabel.htmlFor = 'new_category_name_input';
        newCategoryLabel.textContent = 'O crear nueva categoría:';
        newCategoryLabel.classList.add('form-label', 'mt-2');
        categorySection.appendChild(newCategoryLabel);

        const newCategoryInput = document.createElement('input');
        newCategoryInput.type = 'text';
        newCategoryInput.id = 'new_category_name_input';
        // console.log("Elemento newCategoryInput creado con ID:", newCategoryInput.id, newCategoryInput);
        newCategoryInput.placeholder = 'Nombre para la nueva categoría';
        newCategoryInput.classList.add('form-control', 'form-control-sm');

        // Autocompletar newCategoryInput si Gemini hizo una suposición que NO existe
        if (data.extracted_data.category_name_guess && !geminiGuessExistsInUserCategories) {
            newCategoryInput.value = data.extracted_data.category_name_guess;
            const suggestionMessage = document.createElement('small');
            suggestionMessage.classList.add('form-text', 'text-muted', 'd-block', 'mb-2');
            suggestionMessage.textContent = `La IA sugiere "${data.extracted_data.category_name_guess}" como nueva categoría. Puedes editarla.`;
            categorySection.insertBefore(suggestionMessage, newCategoryInput);
        }
        categorySection.appendChild(newCategoryInput);

        detailsContainer.appendChild(categorySection);
        responseArea.appendChild(detailsContainer);

        // Botones de Acción
        const actionButtonsDiv = document.createElement('div');
        const confirmButton = document.createElement('button');
        confirmButton.textContent = 'Confirmar Gasto';
        confirmButton.classList.add('btn', 'btn-success', 'me-2');
        confirmButton.dataset.extractedRaw = JSON.stringify(data.extracted_data); // Contiene _original_user_instruction
        confirmButton.addEventListener('click', handleExpenseConfirmation);
        actionButtonsDiv.appendChild(confirmButton);

        const cancelButton = document.createElement('button');
        cancelButton.textContent = 'Cancelar';
        cancelButton.classList.add('btn', 'btn-secondary');
        cancelButton.addEventListener('click', cancelConfirmation);
        actionButtonsDiv.appendChild(cancelButton);
        responseArea.appendChild(actionButtonsDiv);
    }

    // Función para manejar el clic en "Confirmar Gasto"
    async function handleExpenseConfirmation(event) {
        const button = event.target;
        const originalExtractedData = JSON.parse(button.dataset.extractedRaw);

        // Leer valores ANTES de modificar responseArea
        const categorySelectElement = document.getElementById('category_select_dropdown');
        const newCategoryInputElement = document.getElementById('new_category_name_input');

        // console.log("Inicio handleExpenseConfirmation - categorySelectElement:", categorySelectElement);
        // console.log("Inicio handleExpenseConfirmation - newCategoryInputElement:", newCategoryInputElement);

        if (!categorySelectElement) {
            console.error("FATAL: Elemento 'category_select_dropdown' NO ENCONTRADO al inicio de handleExpenseConfirmation.");
            responseArea.innerHTML = '<p class="error">Error interno (CSD init): No se pudo procesar la categoría.</p>';
            return;
        }
        if (!newCategoryInputElement) {
            console.error("FATAL: Elemento 'new_category_name_input' NO ENCONTRADO al inicio de handleExpenseConfirmation.");
            responseArea.innerHTML = '<p class="error">Error interno (NCI init): No se pudo procesar la categoría.</p>';
            return;
        }

        const selectedCategoryIdValue = categorySelectElement.value;
        const newCategoryName = newCategoryInputElement.value.trim();
        
        responseArea.innerHTML = '<p class="loading">Registrando el gasto...</p>'; // Mostrar estado de carga

        let finalSelectedCategoryId = null;
        if (selectedCategoryIdValue && selectedCategoryIdValue !== "") { // Si hay un valor y no es la opción por defecto vacía
            const parsedId = parseInt(selectedCategoryIdValue, 10);
            if (!isNaN(parsedId)) { // Asegurar que el parseo a número fue exitoso
                finalSelectedCategoryId = parsedId;
            } else {
                console.warn("Advertencia: El valor seleccionado de categoría no es un número válido:", selectedCategoryIdValue);
            }
        }

        const confirmedPayload = {
            description: originalExtractedData.description,
            amount: originalExtractedData.amount,
            transaction_date: originalExtractedData.transaction_date,
            project_name: originalExtractedData.project_name_guess, // Puede ser null
            _original_user_instruction: originalExtractedData._original_user_instruction,
            selected_category_id: finalSelectedCategoryId,
            create_category_with_name: newCategoryName || null // Si newCategoryName es vacío, enviar null
        };
        
        // console.log("Payload para confirmación:", JSON.stringify(confirmedPayload, null, 2));

        // Obtener el token CSRF directamente del DOM aquí, ya que el input original podría no estar en el mismo scope
        const csrfTokenForConfirmation = document.querySelector('form#aiCommandForm [name=csrfmiddlewaretoken]');
        if (!csrfTokenForConfirmation) {
             console.error("Error: Falta token CSRF (input) para confirmación.");
             responseArea.innerHTML = '<p class="error">Error de configuración: No se pudo enviar (falta token CSRF).</p>';
             return;
        }
        const currentCsrfTokenValue = csrfTokenForConfirmation.value;


        try {
            const response = await fetch(window.AI_COMMAND_HANDLER_URL, { // Usar la variable global para la URL
                method: 'POST',
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': currentCsrfTokenValue},
                body: JSON.stringify({
                    action: "confirm_creation",
                    confirmed_data: confirmedPayload
                })
            });

            // console.log("Respuesta del servidor (confirmación):", response.status, response.statusText);
            const responseDataText = await response.text();
            // console.log("Cuerpo de la respuesta (texto):", responseDataText);

            let dataFromServer;
            if (responseDataText) {
                try {
                    dataFromServer = JSON.parse(responseDataText);
                } catch (e) {
                    console.error("Error parseando JSON de respuesta:", e, "Respuesta recibida:", responseDataText);
                    responseArea.innerHTML = `<p class="error">Error: Respuesta inválida del servidor. Contenido: ${responseDataText.substring(0, 200)}...</p>`;
                    return;
                }
            } else {
                console.error("Respuesta del servidor vacía.");
                responseArea.innerHTML = `<p class="error">Error: Respuesta vacía del servidor.</p>`;
                return;
            }

            if (response.ok) {
                if (dataFromServer.type === 'transaction_created') {
                    handleSuccessfulResponse(dataFromServer, true);
                } else if (dataFromServer.error) { // Error controlado devuelto por el backend con status OK
                    responseArea.innerHTML = `<p class="error"><strong>Error al registrar:</strong> ${dataFromServer.error}</p>`;
                } else { // Otro tipo de respuesta OK
                     handleSuccessfulResponse(dataFromServer);
                }
            } else { // Errores HTTP (4xx, 5xx)
                 responseArea.innerHTML = `<p class="error"><strong>Error ${response.status} al registrar:</strong> ${dataFromServer.error || response.statusText || 'Ocurrió un error.'}</p>`;
            }

        } catch (error) { // Errores de red o del propio fetch
            console.error('Error en solicitud de confirmación (catch):', error);
            responseArea.innerHTML = `<p class="error"><strong>Error de conexión o script en confirmación:</strong> ${error.message}</p>`;
        }
    }

    // Función para manejar el clic en "Cancelar"
    function cancelConfirmation() {
        responseArea.innerHTML = 'Operación cancelada. Esperando instrucción...';
    }

    // Función para manejar respuestas exitosas generales
    function handleSuccessfulResponse(data, forceReload = false) {
        let htmlResponse = '';
        const isCreation = data.type === 'project_created' || data.type === 'task_created' || data.type === 'transaction_created';
        if (isCreation) {
            htmlResponse = `<p class="success"><strong>${data.message || 'Operación completada.'}</strong></p>`;
            if (data.project_id) htmlResponse += `<p>ID Proyecto: ${data.project_id}</p>`;
            if (data.task_id) htmlResponse += `<p>ID Tarea: ${data.task_id}</p>`;
            if (data.transaction_id) htmlResponse += `<p>ID Transacción: ${data.transaction_id}</p>`;
        } else { // Mensaje de texto simple de la IA u otra respuesta no-creación
            htmlResponse = `<p>${data.message || 'Respuesta recibida.'}</p>`;
        }
        responseArea.innerHTML = htmlResponse;
        if (isCreation || forceReload) { // Recargar siempre si es una creación o se fuerza
            responseArea.innerHTML += '<p class="loading">Actualizando página...</p>';
            setTimeout(() => { window.location.reload(); }, 1500);
        }
    }

}); // Fin del DOMContentLoaded listener
```

---

## Archivo: `dashboard/templates/dashboard/dashboard.html`

```html
{# D:\trabajo\Propio\IA\programing\TaskFlow\dashboard\templates\dashboard\dashboard.html #}
{% extends "tasks/base.html" %} {# Heredamos de la plantilla base existente #}
{% load l10n %}
{% load tz %}
{% load static %} {# <-- AÑADIDO: Cargar la etiqueta static #}

{% block title %}Dashboard - TaskFlow{% endblock %}

{% block content %}
    {# Sección de la Consola de IA #}
    <section id="ai-console-section" style="margin-bottom: 30px; padding: 20px; background-color: #e9f7fd; border-radius: 5px;">
        <h2>Crear con IA</h2>
        <form id="aiCommandForm"> {# El CSRF token es crucial para las peticiones POST del JS #}
            {% csrf_token %}
            <div>
                <textarea id="instruction" name="instruction" rows="3"
                          placeholder="Describe una acción principal: Crear proyecto 'X', añadir tarea 'Y' a proyecto 'X', o registrar gasto 'Z'..." required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Enviar Instrucción</button>
        </form>
        <div id="responseArea" class="mt-3">
            Esperando instrucción...
        </div>
        <small class="form-text text-muted mt-2">Consejo: Intenta una acción principal por cada instrucción para mejores resultados.</small>
    </section>
    {# Fin Sección de la Consola de IA #}

    <hr style="margin: 30px 0;">

    {# Estructura de dos columnas con Bootstrap #}
    <div class="row">
        {# Columna Izquierda: Proyectos #}
        <div class="col-md-6">
            <section id="projects-section">
                <h2>Mis Proyectos</h2>
                {% if projects %}
                    <ul class="project-list" style="padding-left: 0; list-style: none;">
                        {% for project in projects %}
                            <li class="project-list-item" style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin-bottom: 15px; border-radius: 5px;">
                                <h3>
                                    <a href="{% url 'tasks:project_detail' pk=project.pk %}">{{ project.name }}</a>
                                </h3>
                                {% if project.description %}
                                    <p style="font-size: 0.9em; color: #6c757d;">{{ project.description }}</p>
                                {% endif %}

                                <h4>Tareas:</h4>
                                {% if project.task_set.all %}
                                    <ul class="task-list">
                                        {% for task in project.task_set.all %}
                                            <li class="task-list-item" style="padding: 5px 0; border-bottom: 1px dashed #e0e0e0;">
                                                 {{ task.description }}
                                                <span style="font-size: 0.8em; color: #6c757d;">
                                                    (Estado: {{ task.get_status_display }})
                                                    {% if task.due_date %} - Vence: {{ task.due_date|date:"d M Y" }}{% endif %}
                                                </span>
                                            </li>
                                            {% if forloop.last %}<style>.task-list-item:last-child { border-bottom: none; }</style>{% endif %}
                                        {% endfor %}
                                    </ul>
                                {% else %}
                                    <p style="font-size: 0.9em; color: #6c757d;">Este proyecto aún no tiene tareas.</p>
                                {% endif %}
                                <p style="margin-top:10px;"><a href="{% url 'tasks:task_create' project_pk=project.pk %}" style="font-size:0.9em;">Añadir Tarea (Manual)</a></p>
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p>Aún no tienes proyectos. ¡Usa la consola de IA arriba para crear uno!</p>
                {% endif %}
            </section>
        </div> {# Fin Columna Izquierda #}

        {# Columna Derecha: Gastos Recientes #}
        <div class="col-md-6">
            <section id="expenses-section">
                <h2>Mis Gastos Recientes</h2>
                {% if recent_transactions %}
                    <ul class="expense-list" style="padding-left: 0; list-style: none;">
                        {% for transaction in recent_transactions %}
                            <li class="expense-list-item" style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin-bottom: 15px; border-radius: 5px;">
                                <p style="margin-bottom: 5px;"><strong>{{ transaction.description }}</strong></p>
                                <p style="margin-bottom: 5px; font-size: 1.1em; color: #dc3545;">
                                    {{ transaction.amount|floatformat:2 }} €
                                    <span style="font-size: 0.8em; color: #6c757d; margin-left: 10px;">
                                        ({{ transaction.transaction_date|date:"d M Y" }})
                                    </span>
                                </p>
                                <p style="font-size: 0.9em; color: #6c757d; margin-bottom: 0;">
                                    {% if transaction.category %}
                                        Categoría: {{ transaction.category.name }}
                                    {% else %}
                                        Sin categoría
                                    {% endif %}
                                    {% if transaction.project %}
                                        | Proyecto: {{ transaction.project.name }}
                                    {% endif %}
                                </p>
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p>Aún no tienes gastos registrados.</p>
                {% endif %}
            </section>
        </div> {# Fin Columna Derecha #}
    </div> {# Fin .row #}

{% endblock %}

{% block javascript %}
{# --- MODIFICADO: Ahora solo definimos variables globales y enlazamos el script externo --- #}
<script>
    // Pasar URLs de Django al scope global de JavaScript para que el script externo las pueda usar.
    // El script dashboard_logic.js esperará que esta variable esté definida.
    window.AI_COMMAND_HANDLER_URL = "{% url 'tasks:ai_command_handler' %}";
</script>
{# Incluir el archivo JavaScript externo. Django lo buscará en dashboard/static/dashboard/js/dashboard_logic.js #}
<script src="{% static 'dashboard/js/dashboard_logic.js' %}"></script>
{# --- FIN MODIFICADO --- #}
{% endblock %}
```

---

## Archivo: `dashboard/tests.py`

```python
from django.test import TestCase

# Create your tests here.

```

---

## Archivo: `dashboard/views.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\dashboard\views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Importar modelos de otras apps
from tasks.models import Project
from accounting.models import Transaction

@login_required
def dashboard_view(request):
    """
    Vista principal del dashboard que muestra un resumen de proyectos
    y gastos recientes.
    """
    # Obtener proyectos con sus tareas precargadas
    projects = Project.objects.filter(user=request.user).prefetch_related('task_set').order_by('name')

    # Obtener las últimas 5 transacciones (gastos)
    recent_transactions = Transaction.objects.filter(
        user=request.user,
        type='expense'
    ).select_related('category', 'project').order_by('-transaction_date', '-created_at')[:5]

    context = {
        'projects': projects,
        'recent_transactions': recent_transactions,
        # Aquí podríamos añadir más datos en el futuro (ej. tareas_proximas, etc.)
    }
    # Renderizará una nueva plantilla que crearemos a continuación
    return render(request, 'dashboard/dashboard.html', context)
```

---

## Archivo: `manage.py`

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskFlowProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

```

---

## Archivo: `requirements.txt`

```text
[Contenido de 'requirements.txt' omitido (Binario, error de codificación/lectura)]
```

---

## Archivo: `start.bat`

```
@echo off
REM Nombre del script: start_dev_server.bat
REM Propósito: Activa el entorno virtual de Python y arranca el servidor de desarrollo de Django.

REM --- CONFIGURACIÓN (Ajusta estas variables si es necesario) ---

REM Ruta al directorio del entorno virtual (relativa a la ubicación de este script .bat)
REM Asume que el venv está en una carpeta llamada "venv" o ".venv" dentro del directorio del proyecto.
SET VENV_DIR=venv

REM Nombre del script de activación del venv (generalmente 'activate.bat' en Windows)
SET VENV_ACTIVATE_SCRIPT=%VENV_DIR%\Scripts\activate.bat

REM Puerto para el servidor de desarrollo de Django (opcional, Django usa 8000 por defecto)
REM SET DJANGO_PORT=8000

REM Dirección IP para el servidor (opcional, 127.0.0.1 por defecto)
REM SET DJANGO_IP=127.0.0.1

REM --- FIN CONFIGURACIÓN ---

ECHO Iniciando TaskFlow Development Server...
ECHO.

REM Verificar si el directorio del proyecto actual es correcto (donde está manage.py)
IF NOT EXIST manage.py (
    ECHO ERROR: No se encontró 'manage.py' en el directorio actual.
    ECHO Asegúrate de ejecutar este script desde la raíz de tu proyecto Django.
    PAUSE
    EXIT /B 1
)

REM Verificar si existe el script de activación del venv
IF NOT EXIST "%VENV_ACTIVATE_SCRIPT%" (
    ECHO ERROR: No se encontró el script de activación del entorno virtual en:
    ECHO %VENV_ACTIVATE_SCRIPT%
    ECHO.
    ECHO Asegúrate de que el entorno virtual '%VENV_DIR%' exista y esté correctamente configurado.
    ECHO Si tu venv tiene otro nombre o ubicación, ajusta la variable VENV_DIR en este script.
    PAUSE
    EXIT /B 1
)

REM Activar el entorno virtual
ECHO Activando entorno virtual: %VENV_DIR%
CALL "%VENV_ACTIVATE_SCRIPT%"

IF ERRORLEVEL 1 (
    ECHO ERROR: Falló la activación del entorno virtual.
    PAUSE
    EXIT /B 1
)

ECHO Entorno virtual activado.
ECHO.

REM Navegar al directorio del proyecto Django si este script no está ya allí
REM (Esto es redundante si el script está en la raíz y ya verificamos manage.py,
REM pero lo dejamos por si se mueve el .bat a una subcarpeta del proyecto)
REM cd /d "%~dp0"

REM Iniciar el servidor de desarrollo de Django
ECHO Iniciando servidor de desarrollo de Django...
ECHO (Presiona CTRL+C para detener el servidor)
ECHO.

REM Construir el comando para runserver con IP y puerto opcionales
SET RUNSERVER_COMMAND=python manage.py runserver
IF DEFINED DJANGO_IP (
    IF DEFINED DJANGO_PORT (
        SET RUNSERVER_COMMAND=%RUNSERVER_COMMAND% %DJANGO_IP%:%DJANGO_PORT%
    ) ELSE (
        SET RUNSERVER_COMMAND=%RUNSERVER_COMMAND% %DJANGO_IP%:8000
    )
) ELSE (
    IF DEFINED DJANGO_PORT (
        SET RUNSERVER_COMMAND=%RUNSERVER_COMMAND% %DJANGO_PORT%
    )
)

REM Ejecutar el comando
%RUNSERVER_COMMAND%

ECHO.
ECHO Servidor de desarrollo detenido.

REM Opcional: Desactivar el entorno virtual (generalmente no es necesario ya que el cmd se cierra o vuelve al prompt original)
REM CALL deactivate

REM PAUSE
EXIT /B 0
```

---

## Archivo: `tasks/__init__.py`

```python

```

---

## Archivo: `tasks/admin.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\admin.py

from django.contrib import admin
from .models import Project, Task # Importamos nuestros modelos

# Registramos el modelo Project en el sitio de administración.
admin.site.register(Project)

# Registramos el modelo Task en el sitio de administración.
admin.site.register(Task)

# Opcional pero recomendado para mejor visualización:
# Podemos crear clases ModelAdmin para personalizar la apariencia en el admin.
# Esto refina la interfaz de control del sistema.

# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('name', 'user', 'created_at') # Campos a mostrar en la lista
#     search_fields = ('name', 'description') # Campos por los que se puede buscar

# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('description', 'project', 'status', 'due_date', 'completed_at')
#     list_filter = ('status', 'project', 'due_date') # Filtros en la barra lateral
#     search_fields = ('description',)

# # Re-registramos usando las clases ModelAdmin personalizadas si las defines
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Task, TaskAdmin)
```

---

## Archivo: `tasks/apps.py`

```python
from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

```

---

## Archivo: `tasks/forms.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\forms.py

from django import forms
# Importamos ambos modelos ahora, ya que ambos tendrán formularios asociados
from .models import Project, Task # <-- Asegúrate de importar Task

class ProjectForm(forms.ModelForm):
    """
    Formulario basado en el modelo Project para crear o actualizar proyectos.
    """
    class Meta:
        model = Project
        # Incluimos solo los campos que el usuario puede editar directamente
        fields = ['name', 'description']
        # Excluimos 'user' porque lo asignaremos automáticamente en la vista
        # Excluimos 'created_at' porque auto_now_add lo maneja
        # exclude = ['user', 'created_at'] # Esta sería otra forma de hacerlo
        
# NUEVO: Formulario para el modelo Task
class TaskForm(forms.ModelForm):
    """
    Formulario basado en el modelo Task para crear o actualizar tareas.
    """
    class Meta:
        model = Task
        # Listamos los campos del modelo Task que queremos incluir en el formulario.
        # 'description' y 'due_date' son los campos que el usuario introducirá.
        # Incluiremos 'status' para permitir al usuario establecer el estado inicial
        fields = ['description', 'status', 'due_date']
        # Excluimos 'project' porque lo asignaremos en la vista basándonos en la URL.
        # Excluimos 'created_at' y 'completed_at' porque se manejan automáticamente o en la lógica de la vista.
        # exclude = ['project', 'created_at', 'completed_at'] # Otra forma con exclude
```

---

## Archivo: `tasks/migrations/0001_initial.py`

```python
# Generated by Django 5.2 on 2025-05-07 02:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('todo', 'Por hacer'), ('doing', 'En progreso'), ('done', 'Completada')], default='todo', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.project')),
            ],
        ),
    ]

```

---

## Archivo: `tasks/migrations/0002_project_original_instruction_and_more.py`

```python
# Generated by Django 5.2 on 2025-05-13 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='original_instruction',
            field=models.TextField(blank=True, help_text='La instrucción original del usuario si fue creado vía IA.', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='original_instruction',
            field=models.TextField(blank=True, help_text='La instrucción original del usuario si fue creado vía IA.', null=True),
        ),
    ]

```

---

## Archivo: `tasks/migrations/__init__.py`

```python

```

---

## Archivo: `tasks/models.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Necesario si usamos completed_at con auto_now

# Entidad Proyecto: El contenedor principal.
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # --- AÑADIDO ---
    original_instruction = models.TextField(
        null=True,
        blank=True,
        help_text="La instrucción original del usuario si fue creado vía IA."
    )
    # --- FIN AÑADIDO ---

    def __str__(self):
        return f"{self.name} (by {self.user.username})"

# Entidad Tarea: Lo que queremos gestionar, contenido dentro de un proyecto.
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Por hacer'),
        ('doing', 'En progreso'),
        ('done', 'Completada'),
    ]

    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    # --- AÑADIDO ---
    original_instruction = models.TextField(
        null=True,
        blank=True,
        help_text="La instrucción original del usuario si fue creado vía IA."
    )
    # --- FIN AÑADIDO ---

    def __str__(self):
        return f"{self.description[:50]}... (Status: {self.status})"

    def mark_as_completed(self):
        if self.status != 'done':
            self.status = 'done'
            # Usar timezone.now() para la consistencia con auto_now_add
            self.completed_at = timezone.now()
            self.save()

    def mark_as_todo(self): # Ejemplo de otra acción
        if self.status == 'done':
            self.status = 'todo'
            self.completed_at = None
            self.save()
```

---

## Archivo: `tasks/services.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\services.py

from django.contrib.auth.models import User
from .models import Project, Task
from django.shortcuts import get_object_or_404
# from django.utils import timezone # No se usa directamente aquí ahora mismo
# from datetime import date

# --- MODIFICADO: create_project_for_user ---
def create_project_for_user(
    user_obj: User,
    name: str,
    description: str = None,
    original_instruction: str = None # <-- AÑADIDO parámetro
) -> Project:
    """
    Crea un nuevo objeto Project asociado a un usuario dado.
    """
    if not isinstance(user_obj, User):
        raise ValueError("Invalid user object provided.")
    if not name:
        raise ValueError("Project name cannot be empty.")

    project = Project(
        user=user_obj,
        name=name,
        description=description,
        original_instruction=original_instruction # <-- AÑADIDO asignación
    )
    project.save()

    print(f"DEBUG: Project '{name}' created for user {user_obj.username}. Instruction: '{original_instruction if original_instruction else 'N/A'}'")
    return project
# --- FIN MODIFICADO ---

# --- MODIFICADO: create_task_for_project ---
def create_task_for_project(
    project_obj: Project,
    description: str,
    status: str = 'todo',
    due_date=None,
    original_instruction: str = None # <-- AÑADIDO parámetro
) -> Task:
    """
    Crea un nuevo objeto Task asociado a un proyecto dado.
    """
    if not isinstance(project_obj, Project):
        raise ValueError("Invalid project object provided.")
    if not description:
        raise ValueError("Task description cannot be empty.")

    task = Task(
        project=project_obj,
        description=description,
        status=status,
        due_date=due_date,
        original_instruction=original_instruction # <-- AÑADIDO asignación
    )
    task.save()

    print(f"DEBUG: Task '{description[:20]}...' created for project '{project_obj.name}'. Instruction: '{original_instruction if original_instruction else 'N/A'}'")
    return task
# --- FIN MODIFICADO ---

def get_project_by_user_and_name(user_obj: User, project_name: str) -> Project:
     """
     Busca un proyecto por nombre para un usuario específico.
     Lanza Project.DoesNotExist o Project.MultipleObjectsReturned si no se encuentra o hay duplicados.
     """
     if not isinstance(user_obj, User):
         raise ValueError("Invalid user object provided.")
     if not project_name:
         raise ValueError("Project name cannot be empty for lookup.")
     return get_object_or_404(Project, user=user_obj, name=project_name)
```

---

## Archivo: `tasks/templates/tasks/base.html`

```html
{# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\templates\tasks\base.html #}
<!DOCTYPE html>
<html lang="es">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    {# --- AÑADIDO: CDN de FontAwesome --- #}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    {# --- FIN AÑADIDO --- #}
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TaskFlow{% endblock %}</title>
    <style>
        /* ... (tus estilos CSS existentes) ... */
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            color: #212529;
            line-height: 1.6;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .header {
            background-color: #343a40;
            color: white;
            padding: 1rem 2rem;
            text-align: center;
        }
        .header h1 { margin: 0; font-size: 2.5rem; }
        .header a { color: white; text-decoration: none; }

        .nav-main {
            background-color: #495057;
            padding: 0.75rem 2rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .nav-main a {
            color: #f8f9fa;
            margin: 0 15px;
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 0;
            border-bottom: 2px solid transparent;
            transition: border-color 0.2s ease-in-out, color 0.2s ease-in-out;
        }
        .nav-main a:hover, .nav-main a.active {
            color: #ffffff;
            border-bottom-color: #0d6efd;
        }

        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto 2rem auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.075);
            flex-grow: 1;
        }
        textarea#instruction { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ced4da; border-radius: 4px; min-height: 60px; font-size: 1rem; }
        #responseArea { margin-top: 15px; padding: 15px; border: 1px solid #e9ecef; border-radius: 4px; background-color: #e9ecef; min-height: 40px; white-space: pre-wrap; font-family: monospace; }
        .loading { color: #007bff; }
        .error { color: #dc3545; font-weight: bold; }
        .success { color: #28a745; font-weight: bold; }

        h1, h2, h3 { color: #343a40; }
        ul { list-style-type: none; padding-left: 0; }
        li { margin-bottom: 0.5em; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }

        .project-list-item, .expense-list-item {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            list-style: none;
        }
        .project-list-item h3, .expense-list-item h3 { margin-top: 0; }
        .project-list-item h3 a { color: #0056b3; }
        .task-list { margin-left: 20px; margin-top: 10px; padding-left: 0; list-style: none;}
        .task-list-item {
            padding: 5px 0;
            border-bottom: 1px dashed #e0e0e0;
            list-style: none;
        }
        .task-list-item:last-child { border-bottom: none; }

        footer {
            text-align: center;
            padding: 1rem;
            background-color: #343a40;
            color: #adb5bd;
            font-size: 0.9em;
            margin-top: auto;
        }
    </style>
    {% block head_extra %}{% endblock %}
</head>
<body>
    <header class="header">
        <h1><a href="{% url 'dashboard' %}">TaskFlow</a></h1>
    </header>

    <nav class="nav-main">
        <a href="{% url 'dashboard' %}">Dashboard</a>
        <a href="{% url 'tasks:project_list' %}">Mis Proyectos</a>
        <a href="{% url 'accounting:transaction_list' %}">Mis Gastos</a>
        <a href="{% url 'accounting:transaction_create' %}">Registrar Gasto</a>
        {% if user.is_authenticated %}
            <span style="color: #adb5bd; margin-left: auto; padding-right: 15px;">Hola, {{ user.username }}!</span>
        {% endif %}
    </nav>

    <main class="container">
        {% block content %}{% endblock %}
    </main>

    <footer>
        TaskFlow &copy; {% now "Y" %} - Tu Asistente Inteligente de Tareas y Proyectos.
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    {% block javascript %}{% endblock %}
</body>
</html>
```

---

## Archivo: `tasks/templates/tasks/project_detail.html`

```html
{# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\templates\tasks\project_detail.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{{ project.name }} - Tareas</title>
</head>
<body>
    <h1>{{ project.name }}</h1>
    <p>{{ project.description }}</p>

    <h2>Tareas</h2>
      <p><a href="{% url 'tasks:task_create' project_pk=project.pk %}">Añadir Nueva Tarea</a></p> {# <-- Añade esta línea #}

    {% if tasks %}
        <ul>
            {% for task in tasks %}
                <li>
                    {{ task.description }} (Estado: {{ task.get_status_display }})
                    {% if task.due_date %} - Vence: {{ task.due_date }}{% endif %}
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Este proyecto aún no tiene tareas.</p>
         <p><a href="{% url 'tasks:task_create' project_pk=project.pk %}">Añadir la primera tarea a este proyecto</a></p>
    {% endif %}

    <p><a href="{% url 'tasks:project_list' %}">Volver a la lista de proyectos</a></p>

</body>
</html>
```

---

## Archivo: `tasks/templates/tasks/project_form.html`

```html
{# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\templates\tasks\project_form.html #}
<!DOCTYPE html>
<html>
<head>
    <title>Crear Nuevo Proyecto</title>
    <style>
        .errorlist {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Crear Nuevo Proyecto</h1>

    <form method="post" action="{% url 'tasks:project_create' %}">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Guardar Proyecto</button>
    </form>

    <p><a href="{% url 'tasks:project_list' %}">Cancelar y volver a la lista</a></p>

</body>
</html>
```

---

## Archivo: `tasks/templates/tasks/project_list.html`

```html
{# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\templates\tasks\project_list.html #}
{% extends "tasks/base.html" %}

{% block title %}Mis Proyectos - TaskFlow{% endblock %}

{% block content %}
    {# Esta página ahora solo muestra la lista de proyectos #}
    <section id="projects-section">
        <h2>Mis Proyectos</h2>
         <p><a href="{% url 'tasks:project_create' %}" class="btn btn-primary mb-3">Crear Nuevo Proyecto (Manual)</a></p>

        {% if projects %}
            <ul class="project-list" style="padding-left: 0; list-style: none;">
                {% for project in projects %}
                    <li class="project-list-item" style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin-bottom: 15px; border-radius: 5px;">
                        <h3>
                            <a href="{% url 'tasks:project_detail' pk=project.pk %}">{{ project.name }}</a>
                        </h3>
                        {% if project.description %}
                            <p style="font-size: 0.9em; color: #6c757d;">{{ project.description }}</p>
                        {% endif %}

                        <h4>Tareas:</h4>
                        {% if project.task_set.all %}
                            <ul class="task-list">
                                {% for task in project.task_set.all %}
                                    <li class="task-list-item" style="padding: 5px 0; border-bottom: 1px dashed #e0e0e0;">
                                         {{ task.description }}
                                        <span style="font-size: 0.8em; color: #6c757d;">
                                            (Estado: {{ task.get_status_display }})
                                            {% if task.due_date %} - Vence: {{ task.due_date|date:"d M Y" }}{% endif %}
                                        </span>
                                    </li>
                                    {% if forloop.last %}
                                        <style>
                                        .task-list-item:last-child { border-bottom: none; }
                                        </style>
                                    {% endif %}
                                {% endfor %}
                            </ul>
                        {% else %}
                            <p style="font-size: 0.9em; color: #6c757d;">Este proyecto aún no tiene tareas.</p>
                        {% endif %}
                        <p style="margin-top:10px;"><a href="{% url 'tasks:task_create' project_pk=project.pk %}" style="font-size:0.9em;">Añadir Tarea (Manual)</a></p>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <p>Aún no tienes proyectos.</p>
        {% endif %}
    </section>

{% endblock %}

{# --- CORREGIDO: Eliminado el bloque javascript de aquí --- #}
{% block javascript %}
{# Ya no se necesita el JS de la consola de IA aquí #}
{% endblock %}
```

---

## Archivo: `tasks/templates/tasks/task_form.html`

```html
{# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\templates\tasks\task_form.html #}
<!DOCTYPE html>
<html>
<head>
    <title>Añadir Tarea a {{ project.name }}</title>
    <style>
        .errorlist {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Añadir Tarea a Proyecto: "{{ project.name }}"</h1>

    <form method="post" action="{% url 'tasks:task_create' project_pk=project.pk %}">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Guardar Tarea</button>
    </form>

    <p><a href="{% url 'tasks:project_detail' pk=project.pk %}">Cancelar y volver al proyecto</a></p>

</body>
</html>
```

---

## Archivo: `tasks/tests.py`

```python
from django.test import TestCase

# Create your tests here.

```

---

## Archivo: `tasks/urls.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\urls.py

from django.urls import path
from . import views

# Namespace para evitar colisiones de nombres de URL si tienes muchas apps
app_name = 'tasks'

urlpatterns = [
    # URL para la lista de proyectos
    path('projects/', views.project_list, name='project_list'),

    # URL para crear un nuevo proyecto
    path('projects/new/', views.project_create, name='project_create'),

    # URL para ver los detalles de un proyecto específico
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),

    # URL para crear una nueva tarea dentro de un proyecto específico
    path('projects/<int:project_pk>/tasks/new/', views.task_create, name='task_create'),

    # URL para el endpoint de comandos de IA (API)
    path('ai-command/', views.ai_command_handler, name='ai_command_handler'),
]
```

---

## Archivo: `tasks/views.py`

```python
# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import os
from datetime import datetime
import traceback
from django.utils import timezone

# Importaciones de Gemini
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException

# Modelos de Tasks
from .models import Project, Task
# Formularios de Tasks
from .forms import ProjectForm, TaskForm
# Servicios de Tasks
from .services import create_project_for_user, create_task_for_project, get_project_by_user_and_name

# Importaciones de Accounting
from accounting.models import Category # <-- Necesario para obtener las categorías del usuario
from accounting.services import create_transaction_from_data


# Vista project_list simplificada
@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user).prefetch_related('task_set').order_by('name')
    context = {'projects': projects}
    return render(request, 'tasks/project_list.html', context)

# Vistas de detalle, creación manual de proyecto y tarea
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    tasks = project.task_set.all().order_by('due_date', 'created_at')
    context = {'project': project, 'tasks': tasks}
    return render(request, 'tasks/project_detail.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('tasks:project_list')
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_form.html', {'form': form})

@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('tasks:project_detail', pk=project.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'project': project})

# Declaraciones de funciones Gemini (sin cambios)
GEMINI_FUNCTION_DECLARATIONS = [
     {
        "name": "create_project",
        "description": "Crea un nuevo proyecto para el usuario. Útil cuando el usuario quiere iniciar un nuevo proyecto, plan o contenedor de tareas.",
        "parameters": { "type": "OBJECT", "properties": { "name": { "type": "STRING", "description": "El nombre del proyecto." }, "description": { "type": "STRING", "description": "Una descripción detallada del proyecto (opcional)." } }, "required": ["name"] }
    },
    {
        "name": "create_task",
        "description": "Crea una nueva tarea y la asigna a un proyecto existente del usuario. Útil cuando el usuario quiere añadir una nueva tarea, ítem por hacer, o acción a un proyecto.",
        "parameters": { "type": "OBJECT", "properties": { "project_name": { "type": "STRING", "description": "El nombre del proyecto existente al que pertenece la tarea." }, "description": { "type": "STRING", "description": "La descripción de la tarea a realizar." }, "status": { "type": "STRING", "description": "El estado actual de la tarea. Valores permitidos: 'todo', 'doing', 'done'. Por defecto es 'todo' si no se especifica.", "enum": ["todo", "doing", "done"] }, "due_date": { "type": "STRING", "description": "La fecha de vencimiento de la tarea en formato AAAA-MM-DD (opcional)." } }, "required": ["project_name", "description"] }
    },
    {
        "name": "extract_expense_data",
        "description": "Extrae la información detallada de un gasto o transacción financiera a partir de la instrucción del usuario. El objetivo es recopilar los detalles para una posterior confirmación antes de registrar el gasto. Se le proveerá la fecha actual como contexto.",
        "parameters": { "type": "OBJECT", "properties": { "description": { "type": "STRING", "description": "La descripción detallada del gasto (ej. 'Almuerzo con cliente X', 'Compra de licencia de software Y')." }, "amount": { "type": "NUMBER", "description": "El monto numérico del gasto (ej. 25.50, 100)." }, "transaction_date": { "type": "STRING", "description": "La fecha en que se realizó el gasto, en formato AAAA-MM-DD (ej. '2024-07-15'). Si el usuario menciona una fecha relativa (ayer, hoy, mañana), debe ser resuelta a una fecha absoluta AAAA-MM-DD basada en la fecha actual proporcionada." }, "category_name_guess": { "type": "STRING", "description": "El nombre de una categoría DE GASTOS *existente* a la que este gasto podría pertenecer (ej. 'Comida', 'Transporte', 'Software'). Si el usuario no menciona una categoría o si la categoría mencionada no parece existir, este campo puede omitirse o dejarse vacío." }, "project_name_guess": { "type": "STRING", "description": "El nombre de un proyecto *existente* al que este gasto podría estar asociado. Si el usuario no menciona un proyecto o si el gasto parece personal, omite este campo." } }, "required": ["description", "amount"] }
    }
]

# Vista del manejador de comandos IA
@login_required
@require_POST
def ai_command_handler(request):
    user_instruction_original = None
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("ERROR: GOOGLE_API_KEY no encontrada.")
            return JsonResponse({'error': 'API Key no configurada.'}, status=500)
        genai.configure(api_key=api_key)

        try:
            data = json.loads(request.body)
            action = data.get('action')
            if 'instruction' in data:
                user_instruction_original = data.get('instruction')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)

        if action == 'confirm_creation':
            confirmed_data = data.get('confirmed_data')
            if not confirmed_data:
                 return JsonResponse({'error': 'Datos de confirmación no proporcionados.'}, status=400)
            print(f"DEBUG: [AI Handler] Recibida confirmación con datos: {confirmed_data}")
            original_instruction_for_expense = confirmed_data.pop('_original_user_instruction', None)
            
            # --- MODIFICADO: Extraer los nuevos campos de categoría del frontend ---
            selected_category_id = confirmed_data.get('selected_category_id')
            create_category_name = confirmed_data.get('create_category_with_name')
            # --- FIN MODIFICADO ---

            try:
                transaction = create_transaction_from_data(
                    user=request.user,
                    description=confirmed_data.get('description'),
                    amount=confirmed_data.get('amount'),
                    transaction_date_str=confirmed_data.get('transaction_date'),
                    # --- MODIFICADO: Pasar nuevos parámetros de categoría al servicio ---
                    selected_category_id=selected_category_id,
                    create_category_with_name=create_category_name,
                    # project_name sigue igual
                    project_name=confirmed_data.get('project_name'),
                    # --- FIN MODIFICADO ---
                    original_instruction=original_instruction_for_expense
                )
                return JsonResponse({
                    'message': f"Gasto '{transaction.description[:30]}...' registrado exitosamente.",
                    'transaction_id': transaction.id,
                    'type': 'transaction_created'
                    })
            except (ValueError, TypeError) as e:
                print(f"ERROR: [AI Handler] Error al crear transacción: {str(e)}")
                return JsonResponse({'error': f"Error al registrar el gasto: {str(e)}"}, status=400)

        if not user_instruction_original:
             return JsonResponse({'error': 'Instrucción no proporcionada para procesar por IA.'}, status=400)

        current_server_date = timezone.localdate().strftime("%Y-%m-%d")
        instruction_for_gemini = f"Contexto: Hoy es {current_server_date}. Mis categorías de gastos existentes son: [{', '.join(c.name for c in Category.objects.filter(user=request.user))}]. Instrucción del usuario: {user_instruction_original}"
        
        print(f"DEBUG: [AI Handler] Enviando a Gemini (con contexto de fecha y categorías): '{instruction_for_gemini}' para {request.user.username}")

        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            tools=GEMINI_FUNCTION_DECLARATIONS,
            safety_settings={
                 HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                 HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                 HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                 HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        chat = model.start_chat(enable_automatic_function_calling=False)
        response = chat.send_message(instruction_for_gemini)

        if not response.candidates or not response.candidates[0].content.parts:
            print(f"DEBUG: [AI Handler] Respuesta Gemini inesperada: {response.prompt_feedback}")
            if response.prompt_feedback and response.prompt_feedback.block_reason == 'SAFETY':
                 return JsonResponse({'error': 'La instrucción fue bloqueada por motivos de seguridad.'}, status=400)
            return JsonResponse({'message': response.text if hasattr(response, 'text') else 'Respuesta IA no clara.'})

        try:
            function_call_part = response.candidates[0].content.parts[0]
            function_call = getattr(function_call_part, 'function_call', None)
        except IndexError:
             print(f"DEBUG: [AI Handler] Respuesta Gemini sin 'parts'.")
             return JsonResponse({'message': response.text if hasattr(response, 'text') else 'Respuesta IA no procesable.'})

        if function_call:
            function_name = function_call.name
            args_dict = {key: value for key, value in function_call.args.items()}
            print(f"DEBUG: [AI Handler] Gemini quiere llamar a '{function_name}' con args: {args_dict}")

            if function_name == "create_project":
                # ... (sin cambios, solo pasa user_instruction_original)
                project_name = args_dict.get("name")
                description = args_dict.get("description")
                if not project_name: return JsonResponse({'error': "Nombre proyecto faltante (IA)."}, status=400)
                try:
                    project = create_project_for_user(request.user, project_name, description, original_instruction=user_instruction_original)
                    return JsonResponse({'message': f"Proyecto '{project.name}' creado.", 'project_id': project.id, 'type': 'project_created'})
                except ValueError as e: return JsonResponse({'error': f"Error creando proyecto: {str(e)}"}, status=400)


            elif function_name == "create_task":
                # ... (sin cambios, solo pasa user_instruction_original)
                project_name_for_task = args_dict.get("project_name")
                task_description = args_dict.get("description")
                status = args_dict.get("status", "todo")
                due_date_str = args_dict.get("due_date")
                if not project_name_for_task or not task_description: return JsonResponse({'error': "Faltan datos tarea (IA)."}, status=400)
                try:
                    project_obj = get_project_by_user_and_name(request.user, project_name_for_task)
                    parsed_due_date = None
                    if due_date_str:
                        try: parsed_due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        except ValueError: print(f"WARN: Fecha tarea inválida '{due_date_str}'.")
                    task = create_task_for_project(project_obj, task_description, status, parsed_due_date, original_instruction=user_instruction_original)
                    return JsonResponse({'message': f"Tarea '{task.description[:30]}...' añadida a '{project_obj.name}'.", 'task_id': task.id, 'type': 'task_created'})
                except Project.DoesNotExist: return JsonResponse({'error': f"Proyecto '{project_name_for_task}' no encontrado."}, status=404)
                except ValueError as e: return JsonResponse({'error': f"Error creando tarea: {str(e)}"}, status=400)

            elif function_name == "extract_expense_data":
                 description = args_dict.get("description")
                 amount = args_dict.get("amount")
                 if not description or amount is None:
                     return JsonResponse({'error': "IA no extrajo descripción o monto."}, status=400)
                 
                 # --- AÑADIDO: Obtener todas las categorías del usuario ---
                 user_categories_list = list(Category.objects.filter(user=request.user).values('id', 'name').order_by('name'))
                 # --- FIN AÑADIDO ---

                 extracted_data = {
                    "description": description,
                    "amount": amount,
                    "transaction_date": args_dict.get("transaction_date"),
                    "category_name_guess": args_dict.get("category_name_guess"), # La IA puede seguir adivinando
                    "project_name_guess": args_dict.get("project_name_guess"),
                    "_original_user_instruction": user_instruction_original
                 }
                 print(f"DEBUG: [AI Handler] Datos gasto para confirmar: {extracted_data}")
                 return JsonResponse({
                    "action_needed": "confirm_expense",
                    "message": "Por favor, confirma los detalles del gasto extraídos:",
                    "extracted_data": extracted_data,
                    # --- AÑADIDO: Enviar lista de categorías al frontend ---
                    "user_categories": user_categories_list
                 })
            else:
                 print(f"WARN: [AI Handler] Función desconocida: {function_name}")
                 return JsonResponse({'error': f"Función IA desconocida: {function_name}"}, status=400)
        else:
            print(f"DEBUG: [AI Handler] Respuesta texto Gemini: '{response.text if hasattr(response, 'text') else ''}'")
            return JsonResponse({'message': response.text if hasattr(response, 'text') else 'IA no sugirió acción específica.'})

    except StopCandidateException as e:
        print(f"ERROR: [AI Handler] StopCandidateException: Reason={getattr(e, 'finish_reason', 'N/A')}, Message={str(e)}")
        error_message = "La IA no pudo completar la solicitud."
        finish_reason = getattr(e, 'finish_reason', 'UNKNOWN').upper()
        if finish_reason == "MALFORMED_FUNCTION_CALL":
            error_message = "La IA no pudo procesar la instrucción compleja. Por favor, intenta dar instrucciones más simples y separadas (una acción principal a la vez)."
        elif finish_reason == "SAFETY": error_message = "La instrucción fue bloqueada por motivos de seguridad."
        elif finish_reason == "RECITATION": error_message = "Respuesta bloqueada por posible recitación de contenido."
        elif finish_reason == "OTHER": error_message = "Respuesta detenida por razón no especificada por la IA."
        return JsonResponse({'error': error_message}, status=400)
    except Exception as e:
        print(f"CRITICAL ERROR en ai_command_handler: {type(e).__name__} - {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'error': 'Ocurrió un error crítico inesperado en el servidor.'}, status=500)
```

---

## Archivo: `ui.psd`

```text
[Contenido de 'ui.psd' omitido (Binario, error de codificación/lectura)]
```

---

## Lista de Archivos con Contenido Omitido

*(Binarios, errores de codificación/lectura, o errores inesperados durante el procesamiento)*

- `requirements.txt`
- `ui.psd`


