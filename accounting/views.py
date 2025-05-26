# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST # <-- ADDED THIS LINE
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

@login_required
@require_POST
def transaction_delete(request, transaction_pk):
    transaction = get_object_or_404(Transaction, pk=transaction_pk)
    
    # Authorization check: Ensure the user deleting the transaction owns it
    if transaction.user != request.user:
        # Or handle as an Http404 or some other error indicating not authorized.
        # For simplicity, redirecting to transaction list.
        # A message could be added here: messages.error(request, "You are not authorized to delete this transaction.")
        return redirect('accounting:transaction_list')
        
    transaction.delete()
    # Optionally, add a Django messages framework message here
    # messages.success(request, 'Transaction deleted successfully.')
    return redirect('accounting:transaction_list')