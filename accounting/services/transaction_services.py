from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.utils import timezone # For timezone awareness if needed for date parsing

# Corrected import based on project structure
from tasks.models import Project as TaskProject 
from ..models import Transaction, Category

from .exchange_rate_service import get_usd_exchange_rate # To store the daily rate

def create_transaction_from_data(user, description, amount, transaction_date_str,
                                 selected_category_id=None, create_category_with_name=None,
                                 project_name=None, original_instruction=None):
    """
    Creates a transaction from structured data, typically extracted by AI.
    Handles date parsing, category creation/retrieval, and project linking.
    Currently assumes amounts are in ARS.
    """

    # Validate and parse amount
    try:
        transaction_amount = Decimal(amount)
        if transaction_amount <= 0:
            raise ValueError("Transaction amount must be positive.")
    except (InvalidOperation, ValueError) as e:
        raise ValueError(f"Invalid amount: {amount}. Error: {e}")

    # Validate and parse transaction_date
    parsed_date = None
    if transaction_date_str:
        try:
            # Attempt to parse various common date formats if necessary,
            # or stick to one like YYYY-MM-DD.
            parsed_date = datetime.strptime(transaction_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format: {transaction_date_str}. Please use YYYY-MM-DD.")
    else:
        # Default to today if no date is provided
        parsed_date = timezone.localdate()

    # Determine Category
    category_obj = None
    if selected_category_id:
        try:
            category_obj = Category.objects.get(id=selected_category_id, user=user)
        except Category.DoesNotExist:
            raise ValueError(f"Selected category ID {selected_category_id} not found or not owned by user.")
    elif create_category_with_name:
        # Ensure the new category name is not empty or excessively long
        if not create_category_with_name.strip():
            raise ValueError("Category name to create cannot be empty.")
        if len(create_category_with_name) > 100: # Or your model's max_length for name
             raise ValueError("Category name is too long.")
        category_obj, created = Category.objects.get_or_create(
            name=create_category_with_name,
            user=user,
            defaults={'name': create_category_with_name.strip()} # Ensure name is stripped, description is not a field in Category
        )
    # else: category can remain None if neither is provided and your model allows it.

    # Determine Project
    project_obj = None
    if project_name:
        try:
            project_obj = TaskProject.objects.get(name=project_name, user=user)
        except TaskProject.DoesNotExist:
            # Optionally, you could create the project if it doesn't exist,
            # or raise an error as it's done here.
            raise ValueError(f"Project '{project_name}' not found for this user.")

    # Create the transaction - Assumes ARS for now from AI
    current_rate = get_usd_exchange_rate(parsed_date)

    transaction = Transaction.objects.create(
        user=user,
        description=description,
        original_amount=transaction_amount, # Amount is ARS
        currency='ARS',                   # Default to ARS
        amount=transaction_amount,        # ARS amount is same as original
        exchange_rate_usd=current_rate,   # Store the rate of the day
        category=category_obj,
        project=project_obj,
        transaction_date=parsed_date,
        type='expense', # Assuming AI extracted expenses; this might need to be a parameter if income is possible
        original_instruction=original_instruction
    )
    return transaction
