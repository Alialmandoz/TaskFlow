# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\services.py

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from decimal import Decimal, InvalidOperation

from .models import Transaction, Category
from tasks.models import Project

def create_transaction_from_data(
    user: User,
    description: str,
    amount: float | int | str,
    transaction_date_str: str | None, # Este es el que nos interesa
    category_name: str | None,
    project_name: str | None,
    original_instruction: str = None
) -> Transaction:

    # ... (validaciones de user, description, amount) ...
    if not isinstance(user, User):
        raise TypeError("Se requiere un objeto User válido.")
    if not description:
        raise ValueError("La descripción de la transacción no puede estar vacía.")
    if amount is None:
         raise ValueError("El monto de la transacción no puede estar vacío.")

    try:
        decimal_amount = Decimal(str(amount))
        if not decimal_amount.is_finite():
             raise ValueError("El monto proporcionado no es un número finito válido.")
    except (InvalidOperation, ValueError):
        raise ValueError(f"El monto '{amount}' no es un valor numérico válido.")

    # --- MODIFICADO: Añadir logs para depurar la fecha ---
    print(f"DEBUG: [Accounting Service] Intentando procesar fecha. transaction_date_str recibido: '{transaction_date_str}' (Tipo: {type(transaction_date_str)})")
    parsed_date = None
    if transaction_date_str and transaction_date_str.strip(): # Asegurar que no sea solo espacios
        try:
            parsed_date = datetime.strptime(transaction_date_str, "%Y-%m-%d").date()
            print(f"DEBUG: [Accounting Service] Fecha parseada exitosamente: {parsed_date}")
        except ValueError as e:
            print(f"ERROR: [Accounting Service] Falló el parseo de strptime para '{transaction_date_str}': {e}. Usando fecha actual.")
            parsed_date = timezone.now().date()
    else:
        print(f"DEBUG: [Accounting Service] transaction_date_str está vacío o es None. Usando fecha actual.")
        parsed_date = timezone.now().date()
    # --- FIN MODIFICADO ---


    # ... (búsqueda de categoría y proyecto) ...
    category_obj = None
    if category_name:
        try:
            category_obj = Category.objects.get(user=user, name__iexact=category_name)
        except Category.DoesNotExist:
            print(f"WARN: [Accounting Service] Categoría '{category_name}' no encontrada.")

    project_obj = None
    if project_name:
        try:
            project_obj = Project.objects.get(user=user, name__iexact=project_name)
        except Project.DoesNotExist:
            print(f"WARN: [Accounting Service] Proyecto '{project_name}' no encontrado.")


    transaction = Transaction(
        user=user,
        description=description,
        amount=decimal_amount,
        transaction_date=parsed_date, # Usar la fecha procesada
        category=category_obj,
        project=project_obj,
        type='expense',
        original_instruction=original_instruction
    )
    transaction.save()

    print(f"INFO: [Accounting Service] Transacción creada ID: {transaction.id}. Fecha final guardada: {transaction.transaction_date}")
    return transaction