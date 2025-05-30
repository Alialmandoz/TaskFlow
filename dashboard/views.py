# D:\trabajo\Propio\IA\programing\TaskFlow\dashboard\views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# F and Q might not be strictly necessary for this specific implementation if we filter by category__isnull=False,
# but they are good to have for more complex queries.
# from django.db.models import F, Q 
from django.utils import timezone
from datetime import timedelta
# monthrange is not used in the provided snippet, can be omitted for now.
# from calendar import monthrange 

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

    # --- LÓGICA PARA RESUMEN DE GASTOS ---
    today = timezone.localdate()

    # Periodo: Último Mes Completo
    first_day_current_month = today.replace(day=1)
    last_day_last_month = first_day_current_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)

    gastos_ultimo_mes = Transaction.objects.filter(
        user=request.user,
        type='expense',
        transaction_date__gte=first_day_last_month,
        transaction_date__lte=last_day_last_month,
        category__isnull=False # Considerar solo transacciones con categoría
    ).values(
        'category__name' # Agrupar por nombre de categoría
    ).annotate(
        total_gastado=Sum('amount') # Sumar los montos
    ).order_by('-total_gastado') # Opcional: ordenar por el que más gastó

    # Periodo: Año Actual
    first_day_current_year = today.replace(month=1, day=1)

    gastos_ano_actual = Transaction.objects.filter(
        user=request.user,
        type='expense',
        transaction_date__gte=first_day_current_year,
        transaction_date__lte=today, # Hasta el día de hoy
        category__isnull=False
    ).values(
        'category__name'
    ).annotate(
        total_gastado=Sum('amount')
    ).order_by('-total_gastado')
    
    nombre_mes_anterior = last_day_last_month.strftime("%B %Y")
    ano_actual_display = today.year
    # --- FIN LÓGICA RESUMEN DE GASTOS ---

    context = {
        'projects': projects,
        'recent_transactions': recent_transactions,
        'gastos_ultimo_mes': gastos_ultimo_mes,
        'gastos_ano_actual': gastos_ano_actual,
        'nombre_mes_anterior': nombre_mes_anterior,
        'ano_actual_display': ano_actual_display,
        # Aquí podríamos añadir más datos en el futuro (ej. tareas_proximas, etc.)
    }
    # Renderizará una nueva plantilla que crearemos a continuación
    return render(request, 'dashboard/dashboard.html', context)