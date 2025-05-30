# D:\trabajo\Propio\IA\programing\TaskFlow\dashboard\views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# F and Q might not be strictly necessary for this specific implementation if we filter by category__isnull=False,
# but they are good to have for more complex queries.
# from django.db.models import F, Q 
from django.utils import timezone
# from datetime import timedelta # No longer needed for last month calculation directly here
from datetime import date # Added for date object creation
import calendar # For monthrange and month_name

# Importar modelos de otras apps
from tasks.models import Project
from accounting.models import Transaction

# Import new form
from .forms import MonthSelectorForm

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

    # --- LÓGICA PARA RESUMEN DE GASTOS POR MES SELECCIONADO ---
    current_tz_date = timezone.localdate()
    selected_year = current_tz_date.year
    selected_month = current_tz_date.month

    if request.GET:
        month_selector_form = MonthSelectorForm(request.GET)
        if month_selector_form.is_valid():
            selected_year = int(month_selector_form.cleaned_data['year'])
            selected_month = int(month_selector_form.cleaned_data['month'])
    else:
        # Default to current month if no selection
        month_selector_form = MonthSelectorForm(initial={'year': selected_year, 'month': selected_month})

    # Calculate first and last day of the selected month
    _, num_days_in_selected_month = calendar.monthrange(selected_year, selected_month)
    first_day_selected_month = date(selected_year, selected_month, 1)
    last_day_selected_month = date(selected_year, selected_month, num_days_in_selected_month)

    gastos_mes_seleccionado = Transaction.objects.filter(
        user=request.user,
        type='expense',
        transaction_date__gte=first_day_selected_month,
        transaction_date__lte=last_day_selected_month,
        category__isnull=False
    ).values(
        'category__name'
    ).annotate(
        total_gastado=Sum('amount')
    ).order_by('-total_gastado')

    nombre_mes_seleccionado_display = f"{calendar.month_name[selected_month]} {selected_year}"
    # --- FIN LÓGICA RESUMEN DE GASTOS POR MES SELECCIONADO ---

    # --- LÓGICA PARA RESUMEN DE GASTOS DEL AÑO ACTUAL (remains the same) ---
    # today variable is now current_tz_date
    first_day_current_year = current_tz_date.replace(month=1, day=1)
    gastos_ano_actual = Transaction.objects.filter(
        user=request.user,
        type='expense',
        transaction_date__gte=first_day_current_year,
        transaction_date__lte=current_tz_date, # Use current_tz_date
        category__isnull=False
    ).values(
        'category__name'
    ).annotate(
        total_gastado=Sum('amount')
    ).order_by('-total_gastado')
    ano_actual_display = current_tz_date.year # Use current_tz_date
    # --- FIN LÓGICA RESUMEN DE GASTOS DEL AÑO ACTUAL ---

    context = {
        'projects': projects,
        'recent_transactions': recent_transactions,
        'month_selector_form': month_selector_form,
        'gastos_mes_seleccionado': gastos_mes_seleccionado,
        'nombre_mes_seleccionado_display': nombre_mes_seleccionado_display,
        'gastos_ano_actual': gastos_ano_actual,
        'ano_actual_display': ano_actual_display,
        # Aquí podríamos añadir más datos en el futuro (ej. tareas_proximas, etc.)
    }
    # Renderizará una nueva plantilla que crearemos a continuación
    return render(request, 'dashboard/dashboard.html', context)