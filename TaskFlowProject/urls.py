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