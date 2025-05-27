from decimal import Decimal
from datetime import date
# from django.utils import timezone # If needed for date comparisons
# from ..models import Transaction # For 'last known value'

# TODO: Placeholder for actual API integration details
# API_BASE_URL = "YOUR_CHOSEN_API_ENDPOINT_HERE"
# API_KEY = "YOUR_API_KEY_HERE"

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

# Example of how this might be called (for testing the service directly)
# if __name__ == '__main__':
#     # This part is for direct script execution testing, not for Django app usage
#     # To run this directly, you'd need to configure Django settings if models are imported at module level
#     # or ensure this script can run standalone if Django context isn't strictly needed for the placeholder.
#     # For the current version with Transaction import inside the function, Django setup is needed.
#
#     # If you have a Django setup and want to test this script:
#     # import os
#     # import django
#     # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskFlowProject.settings') # Adjust to your project
#     # django.setup()
#
#     from django.utils import timezone # Import here for example usage
#
#     test_date = date(2023, 10, 26)
#     rate = get_usd_exchange_rate(test_date)
#     print(f"Exchange rate for {test_date}: {rate}")
#
#     # Example with a more recent date (e.g., today)
#     # test_date_future = timezone.now().date() # Removed timedelta for simplicity with placeholder
#     # rate_future = get_usd_exchange_rate(test_date_future)
#     # print(f"Exchange rate for {test_date_future}: {rate_future}")
