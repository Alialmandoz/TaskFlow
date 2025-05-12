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