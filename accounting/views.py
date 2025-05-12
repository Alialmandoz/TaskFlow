# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy # Para redirecciones después del éxito
from .forms import TransactionForm # Importamos nuestro nuevo formulario
from .models import Transaction # Importamos el modelo por si necesitamos interactuar directamente

@login_required # Solo usuarios logueados pueden acceder
def transaction_create(request):
    """
    Vista para manejar la creación de nuevas transacciones (gastos).
    """
    if request.method == 'POST':
        # Al instanciar el formulario con datos POST, pasamos el request.user
        # para que el __init__ del formulario pueda filtrar los querysets.
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            # Creamos la instancia de la transacción pero sin guardarla aún (commit=False)
            transaction = form.save(commit=False)
            # Asignamos el usuario actual a la transacción
            transaction.user = request.user
            # Si el tipo es fijo y no está en el form, asignarlo aquí:
            # transaction.type = 'expense' # Aunque ya está en el form con default
            
            transaction.save() # Guardamos la transacción en la base de datos
            
            # Redirigir a alguna página después de guardar exitosamente.
            # Podría ser una lista de transacciones o de vuelta al dashboard.
            # Por ahora, vamos a asumir que tenemos una lista de transacciones más adelante.
            # Si no, podemos redirigir al dashboard de 'tasks'.
            # return redirect('accounting:transaction_list') # Cuando la tengamos
            return redirect(reverse_lazy('tasks:project_list')) # Redirige al dashboard principal por ahora
    else: # Si la solicitud es GET (o cualquier otro método)
        # Al instanciar el formulario vacío para una solicitud GET, también pasamos el request.user
        form = TransactionForm(user=request.user)

    # Renderizamos la plantilla, pasando el formulario.
    # Crearemos 'accounting/transaction_form.html' en el siguiente paso.
    context = {
        'form': form,
        'page_title': 'Registrar Nuevo Gasto' # Título para la plantilla
    }
    return render(request, 'accounting/transaction_form.html', context)

# Aquí iría la vista transaction_list más adelante
# @login_required
# def transaction_list(request):
#     transactions = Transaction.objects.filter(user=request.user)
#     context = {'transactions': transactions}
#     return render(request, 'accounting/transaction_list.html', context)