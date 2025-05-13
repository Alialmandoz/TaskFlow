# D:\trabajo\Propio\IA\programing\TaskFlow\TaskFlowProject\urls.py

from django.contrib import admin
from django.urls import path, include
# --- AÑADIDO: Importar la vista del dashboard ---
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # --- AÑADIDO: URL raíz apunta al dashboard ---
    path('', dashboard_views.dashboard_view, name='dashboard'),
    # Mantener las URLs de las apps específicas con sus prefijos
    path('tasks/', include('tasks.urls')),
    path('accounting/', include('accounting.urls')),
]