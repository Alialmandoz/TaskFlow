from decimal import Decimal, InvalidOperation
from datetime import datetime, date # Add date
from django.utils import timezone # For timezone awareness if needed for date parsing

# Corrected import based on project structure
from tasks.models import Project as TaskProject 
from ..models import Transaction, Category

# Removed: from .exchange_rate_service import get_usd_exchange_rate # To store the daily rate

def create_transaction_from_data(user, description, original_amount, currency='ARS', transaction_date_str=None,
                                 selected_category_id=None, create_category_with_name=None,
                                 project_name=None, original_instruction=None):
    """
    Creates a transaction from structured data, typically extracted by AI.
    Handles date parsing, category creation/retrieval, project linking,
    and currency conversion (USD to ARS).
    """

    # Validate and parse original_amount
    try:
        transaction_original_amount = Decimal(original_amount)
        if transaction_original_amount <= 0:
            raise ValueError("Transaction original_amount must be positive.")
    except (InvalidOperation, ValueError) as e:
        raise ValueError(f"Invalid original_amount: {original_amount}. Error: {e}")

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

    # Currency Handling and ARS Amount Calculation
    currency_code = currency.upper() if currency else 'ARS'
    calculated_ars_amount = transaction_original_amount
    current_exchange_rate = None

    if currency_code == 'USD':
        current_exchange_rate = get_usd_exchange_rate(parsed_date) # Call the local/consolidated function
        calculated_ars_amount = transaction_original_amount * current_exchange_rate
    elif currency_code == 'ARS':
        # Store the day's USDARS rate for informational purposes, even if the transaction is in ARS.
        current_exchange_rate = get_usd_exchange_rate(parsed_date)
        # If currency is ARS, original_amount IS the ARS amount.
    else:
        # For now, if it's not USD, treat as ARS.
        currency_code = 'ARS' 
        current_exchange_rate = get_usd_exchange_rate(parsed_date)

    # Create the transaction
    transaction = Transaction.objects.create(
        user=user,
        description=description,
        original_amount=transaction_original_amount, # Use the validated original_amount
        currency=currency_code,                     # Use the normalized currency_code
        amount=calculated_ars_amount.quantize(Decimal('0.01')), # Store the calculated ARS amount, quantized
        exchange_rate_usd=current_exchange_rate,    # Store the fetched/determined exchange rate
        category=category_obj,
        project=project_obj,
        transaction_date=parsed_date,
        type='expense', # Assuming AI extracted expenses; this might need to be a parameter if income is possible
        original_instruction=original_instruction
    )
    return transaction

def get_usd_exchange_rate(transaction_date):
    """
    Fetches the USD to ARS exchange rate for a given date.
    Currently a placeholder.
    
    Args:
        transaction_date (datetime.date): The date for which to fetch the rate.
        
    Returns:
        Decimal: The exchange rate (ARS per 1 USD).
                 Returns a default/mocked rate if API fails or not implemented.
    """
    
    # TODO: Implement actual API call here.
    # Example structure:
    # try:
    #     response = requests.get(f"{API_BASE_URL}?date={transaction_date}&symbols=ARS&base=USD", headers={"apikey": API_KEY})
    #     response.raise_for_status() # Raise an exception for HTTP errors
    #     data = response.json()
    #     rate = Decimal(data['rates']['ARS'])
    #     # Optional: Store/cache the fetched rate here for future 'last known value' use.
    #     return rate
    # except requests.RequestException as e:
    #     print(f"API request failed: {e}")
    #     # Fallback to 'last known value' or default
    # except (KeyError, ValueError) as e:
    #     print(f"Failed to parse API response: {e}")
    #     # Fallback to 'last known value' or default

    print(f"DEBUG: get_usd_exchange_rate called for {transaction_date}. Using placeholder rate.")

    # Placeholder logic:
    # Attempt to get the most recent rate from existing transactions as a 'last known value'
    # This is a simplified fallback. A more robust solution might involve a dedicated cache or model for rates.
    try:
        # Import Transaction here to avoid circular import issues at module load time,
        # and if services.py is imported by models.py (though it shouldn't be directly).
        from ..models import Transaction 
        latest_transaction_with_rate = Transaction.objects.filter(
            exchange_rate_usd__isnull=False
        ).latest('transaction_date') # or 'date_created' or 'id'
        
        if latest_transaction_with_rate:
            print(f"DEBUG: Using last known rate from transaction on {latest_transaction_with_rate.transaction_date}: {latest_transaction_with_rate.exchange_rate_usd}")
            return latest_transaction_with_rate.exchange_rate_usd
    except Transaction.DoesNotExist:
        print("DEBUG: No existing transactions with rates found.")
    except Exception as e:
        # Catch any other unexpected error during fallback to prevent full failure
        print(f"DEBUG: Error during fallback to last known rate: {e}")

    # Default fallback if API fails and no 'last known value' is found
    default_rate = Decimal('1200.0000') # Matching the data migration default
    print(f"DEBUG: Falling back to default rate: {default_rate}")
    return default_rate
