# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\urls.py

from django.urls import path
from . import views # Importaremos las vistas de esta app

app_name = 'accounting' # Define un namespace para estas URLs

urlpatterns = [
    # URL para añadir una nueva transacción
    path('transaction/add/', views.transaction_create, name='transaction_create'),
    # Más adelante añadiremos la URL para listar transacciones aquí
    # path('transactions/', views.transaction_list, name='transaction_list'),
]