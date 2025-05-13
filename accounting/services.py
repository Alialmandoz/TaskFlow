# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\services.py

# --- AÑADIDO: Archivo completo ---

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from decimal import Decimal, InvalidOperation # Para manejar montos

# Importar modelos locales y de otras apps
from .models import Transaction, Category
from tasks.models import Project

def create_transaction_from_data(
    user: User,
    description: str,
    amount: float | int | str, # Puede venir como número o string del JSON
    transaction_date_str: str | None,
    category_name: str | None,
    project_name: str | None
) -> Transaction:
    """
    Crea y guarda una nueva transacción (gasto) a partir de datos validados.

    Busca categoría y proyecto por nombre (case-insensitive). Si no se encuentran
    o no se proporcionan, los campos correspondientes en la transacción quedan en None.

    Args:
        user: El objeto User al que pertenece la transacción.
        description: Descripción del gasto.
        amount: Monto del gasto.
        transaction_date_str: Fecha en formato 'YYYY-MM-DD' o None.
        category_name: Nombre de la categoría (opcional).
        project_name: Nombre del proyecto (opcional).

    Returns:
        La instancia de Transaction creada y guardada.

    Raises:
        ValueError: Si la descripción o el monto faltan, o si el monto no es numérico.
        TypeError: Si el usuario no es una instancia válida de User.
    """
    # Validación básica de entrada
    if not isinstance(user, User):
        raise TypeError("Se requiere un objeto User válido.")
    if not description:
        raise ValueError("La descripción de la transacción no puede estar vacía.")
    if amount is None:
         raise ValueError("El monto de la transacción no puede estar vacío.")

    # Validar y convertir monto a Decimal
    try:
        decimal_amount = Decimal(str(amount)) # Convertir a string primero por si viene como float
        if not decimal_amount.is_finite(): # Chequear NaN o Infinito
             raise ValueError("El monto proporcionado no es un número finito válido.")
    except (InvalidOperation, ValueError):
        raise ValueError(f"El monto '{amount}' no es un valor numérico válido.")


    # Parsear fecha o usar fecha actual
    parsed_date = None
    if transaction_date_str:
        try:
            parsed_date = datetime.strptime(transaction_date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"WARN: [Accounting Service] Formato de fecha inválido '{transaction_date_str}'. Usando fecha actual.")
            # Podríamos lanzar un error aquí si quisiéramos ser estrictos,
            # pero usar la fecha actual es más permisivo para el usuario.
            parsed_date = timezone.now().date()
    else:
        parsed_date = timezone.now().date() # Default a hoy si no se proporciona

    # Buscar categoría (opcional, case-insensitive)
    category_obj = None
    if category_name:
        try:
            # Usamos iexact para búsqueda case-insensitive
            category_obj = Category.objects.get(user=user, name__iexact=category_name)
            print(f"DEBUG: [Accounting Service] Categoría encontrada: {category_obj.name}")
        except Category.DoesNotExist:
            print(f"WARN: [Accounting Service] Categoría '{category_name}' no encontrada para el usuario {user.username}. Se registrará sin categoría.")
            # No lanzamos error, simplemente no se asigna categoría.

    # Buscar proyecto (opcional, case-insensitive)
    project_obj = None
    if project_name:
        try:
            project_obj = Project.objects.get(user=user, name__iexact=project_name)
            print(f"DEBUG: [Accounting Service] Proyecto encontrado: {project_obj.name}")
        except Project.DoesNotExist:
            print(f"WARN: [Accounting Service] Proyecto '{project_name}' no encontrado para el usuario {user.username}. Se registrará sin proyecto asociado.")
            # No lanzamos error, simplemente no se asigna proyecto.


    # Crear y guardar la transacción
    transaction = Transaction(
        user=user,
        description=description,
        amount=decimal_amount, # Usar el Decimal validado
        transaction_date=parsed_date,
        category=category_obj, # Puede ser None
        project=project_obj,   # Puede ser None
        type='expense' # Asumimos que siempre es gasto por ahora
        # notes se deja vacío (default del modelo)
    )
    transaction.save()

    print(f"INFO: [Accounting Service] Transacción creada con ID: {transaction.id} para usuario {user.username}")
    return transaction

# --- FIN AÑADIDO ---