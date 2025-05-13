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