# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\services.py

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, date as python_date
from decimal import Decimal, InvalidOperation

from .models import Transaction, Category # Category es necesario para crear/buscar
from tasks.models import Project

# --- MODIFICADO: create_transaction_from_data para manejar ID de categoría o creación de nueva categoría ---
def create_transaction_from_data(
    user: User,
    description: str,
    amount: float | int | str,
    transaction_date_str: str | None,
    # Nuevos parámetros para categoría:
    selected_category_id: int | None,
    create_category_with_name: str | None,
    # project_name sigue igual
    project_name: str | None,
    original_instruction: str = None
) -> Transaction:
    """
    Crea y guarda una nueva transacción (gasto).
    Asigna una categoría existente por ID, o crea y asigna una nueva categoría por nombre.
    """
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

    print(f"DEBUG: [Accounting Service] Intentando procesar fecha. transaction_date_str: '{transaction_date_str}'")
    parsed_date_obj: python_date
    if transaction_date_str and transaction_date_str.strip():
        try:
            dt_naive = datetime.strptime(transaction_date_str, "%Y-%m-%d")
            parsed_date_obj = dt_naive.date()
            print(f"DEBUG: [Accounting Service] Fecha parseada de string: {parsed_date_obj}")
        except ValueError as e:
            print(f"ERROR: [Accounting Service] Falló strptime para '{transaction_date_str}': {e}. Usando fecha actual.")
            parsed_date_obj = timezone.localdate()
    else:
        print(f"DEBUG: [Accounting Service] transaction_date_str vacío/None. Usando fecha actual.")
        parsed_date_obj = timezone.localdate()
    print(f"DEBUG: [Accounting Service] Fecha a usar para la transacción: {parsed_date_obj}")

    category_obj = None
    # --- Lógica de Categoría Modificada ---
    if selected_category_id:
        try:
            category_obj = Category.objects.get(pk=selected_category_id, user=user)
            print(f"DEBUG: [Accounting Service] Categoría seleccionada por ID: {category_obj.name}")
        except Category.DoesNotExist:
            print(f"WARN: [Accounting Service] Categoría con ID '{selected_category_id}' no encontrada para el usuario {user.username}. Se ignorará.")
            # Podríamos lanzar un error aquí si el ID debería ser siempre válido.
    elif create_category_with_name and create_category_with_name.strip():
        category_name_cleaned = create_category_with_name.strip()
        # Intentar obtenerla por si ya existe (case-insensitive) para evitar duplicados exactos
        category_obj, created = Category.objects.get_or_create(
            user=user,
            name__iexact=category_name_cleaned, # Buscar ignorando mayúsculas/minúsculas
            defaults={'name': category_name_cleaned, 'user': user} # Asegurar el nombre correcto al crear
        )
        if created:
            print(f"INFO: [Accounting Service] Nueva categoría '{category_obj.name}' creada para el usuario {user.username}.")
        else:
            print(f"DEBUG: [Accounting Service] Categoría existente '{category_obj.name}' encontrada y usada para el nombre '{category_name_cleaned}'.")
    else:
        print(f"DEBUG: [Accounting Service] No se seleccionó ni se creó una categoría.")
    # --- Fin Lógica de Categoría Modificada ---

    project_obj = None
    if project_name:
        try:
            project_obj = Project.objects.get(user=user, name__iexact=project_name)
            print(f"DEBUG: [Accounting Service] Proyecto encontrado: {project_obj.name}")
        except Project.DoesNotExist:
            print(f"WARN: [Accounting Service] Proyecto '{project_name}' no encontrado. Se registrará sin proyecto.")

    transaction = Transaction(
        user=user,
        description=description,
        amount=decimal_amount,
        transaction_date=parsed_date_obj,
        category=category_obj, # Puede ser None, o la seleccionada/creada
        project=project_obj,
        type='expense',
        original_instruction=original_instruction
    )
    transaction.save()

    print(f"INFO: [Accounting Service] Transacción creada ID: {transaction.id}. Fecha: {transaction.transaction_date}. Categoría: {transaction.category.name if transaction.category else 'N/A'}")
    return transaction
# --- FIN MODIFICADO ---