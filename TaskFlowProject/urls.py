# D:\trabajo\Propio\IA\programing\TaskFlow\TaskFlowProject\urls.py

from django.contrib import admin
from django.urls import path, include # Importamos include

urlpatterns = [
    path('admin/', admin.site.urls), # La URL del sitio de administración que ya usamos
    # Incluimos las URLs de nuestra app tasks bajo la ruta base 'tasks/'
    # Esto significa que las URLs definidas en tasks/urls.py (como 'projects/')
    # serán accesibles en '/tasks/projects/', '/tasks/projects/<int:pk>/', etc.
    path('tasks/', include('tasks.urls')),
    # Puedes añadir una ruta raíz si quieres, por ejemplo:
    path('', include('tasks.urls')), # Esto haría que 'projects/' fuera accesible en '/'
    path('accounting/', include('accounting.urls')),
]