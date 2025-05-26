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

    # URL para eliminar una transacción
    path('transaction/<int:transaction_pk>/delete/', views.transaction_delete, name='transaction_delete'),
]