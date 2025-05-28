# Testing Plan: Multi-Currency Expense Feature

This document outlines the testing plan for the multi-currency expense feature in the TaskFlow application.

## I. Model and Data Migrations

1.  **Migration Application:**
    *   **Test Case 1.1:** On a clean database (no previous migrations applied), run `python manage.py migrate`. Verify that all migrations, including `accounting.0003_...` and `accounting.0004_...`, apply successfully without errors.
    *   **Test Case 1.2:** On a database with existing transactions (migrated up to `accounting.0002_...`), run `python manage.py migrate`. Verify that migrations `accounting.0003_...` and `accounting.0004_...` apply successfully without errors.

2.  **Existing Data Population (after migration `0004_...` on a database with pre-existing data):**
    *   **Test Case 2.1:** Query all transactions that existed before the migration. For each transaction, verify `currency` field is set to "ARS".
        *   *Expected Result:* `transaction.currency == "ARS"`.
    *   **Test Case 2.2:** For each of these transactions, verify `original_amount` field is equal to the value previously stored in its `amount` field.
        *   *Expected Result:* `transaction.original_amount == old_transaction.amount`.
    *   **Test Case 2.3:** For each of these transactions, verify `exchange_rate_usd` field is set to `Decimal('1200.0000')`.
        *   *Expected Result:* `transaction.exchange_rate_usd == Decimal('1200.0000')`.

3.  **New Field Defaults (Programmatic Creation):**
    *   **Test Case 3.1:** Create a new `Transaction` object programmatically without specifying `currency`.
        ```python
        # from accounting.models import Transaction, User, Category
        # user = User.objects.first() # Assuming a user exists
        # new_trans = Transaction.objects.create(user=user, description="Test", original_amount=100)
        ```
    *   Verify the default value for `currency` is "ARS".
        *   *Expected Result:* `new_trans.currency == "ARS"`.

## II. Exchange Rate Service (`accounting/services/exchange_rate_service.py`)

1.  **Placeholder Behavior (Current Implementation):**
    *   **Test Case 1.1:** Ensure the database has no transactions or no transactions with `exchange_rate_usd` set. Call `get_usd_exchange_rate(date.today())`.
        *   *Expected Result:* Function returns `Decimal('1200.0000')` (the default rate). The debug log should indicate fallback to default.
    *   **Test Case 1.2:** Programmatically create a transaction:
        ```python
        # from accounting.models import Transaction, User
        # from decimal import Decimal
        # from django.utils import timezone
        # user = User.objects.first()
        # Transaction.objects.create(
        #     user=user, description="Rate Test", currency="USD",
        #     original_amount=Decimal('1.00'), amount=Decimal('1100.00'),
        #     transaction_date=timezone.now().date() - timezone.timedelta(days=1), # A recent date
        #     exchange_rate_usd=Decimal('1100.0000')
        # )
        ```
        Call `get_usd_exchange_rate(date.today())`. (Assuming the "API call" part of the service is still commented out/mocked to fail).
        *   *Expected Result:* Function returns `Decimal('1100.0000')`. The debug log should indicate usage of "last known rate".

2.  **(Future - Actual API Integration):**
    *   **Test Case 2.1:** When a real API is integrated, mock the API response to return a known rate for a specific date. Call `get_usd_exchange_rate(specific_date)`.
        *   *Expected Result:* Function returns the known rate from the API.
    *   **Test Case 2.2:** Call `get_usd_exchange_rate(future_date)` where `future_date` is a date after the current known range of the API.
        *   *Expected Result:* Define expected behavior: Should it error, return the latest known rate from API, or fallback to service's internal default? (e.g., return latest known valid rate).
    *   **Test Case 2.3:** Call `get_usd_exchange_rate(past_date)` where `past_date` is very far in the past (e.g., before API data availability).
        *   *Expected Result:* Define expected behavior (e.g., API might return an error, service falls back to default or last known).
    *   **Test Case 2.4:** Simulate API downtime or an error response (e.g., 500 error, malformed JSON).
        *   *Expected Result:* Service should handle the error gracefully and fall back to "last known rate" or the default rate (`Decimal('1200.0000')`).

## III. Transaction Form and CRUD Operations

1.  **Form Display (`accounting/transaction_form.html`):**
    *   **Test Case 1.1:** Navigate to the transaction creation/edit page.
        *   *Expected Result:* The form displays a field labeled "Amount" (which corresponds to `original_amount`) and a "Currency" dropdown/selection field. The old "Amount" field (representing the ARS value) is not visible for user input.

2.  **Creating ARS Transaction:**
    *   **Test Case 2.1:**
        1.  Go to "Register New Expense" page.
        2.  Enter description.
        3.  For "Amount", enter `500`.
        4.  Select "ARS" from the "Currency" dropdown.
        5.  Enter a valid transaction date.
        6.  Click "Register Expense".
    *   *Expected Result:*
        *   Transaction is saved successfully.
        *   In the database: `original_amount` is `500.00`, `currency` is `"ARS"`, `amount` (ARS value) is `500.00`.
        *   `exchange_rate_usd` is populated with the rate fetched by `get_usd_exchange_rate` for the transaction_date (e.g., `1200.0000` if default).

3.  **Creating USD Transaction:**
    *   **Test Case 3.1:**
        1.  Go to "Register New Expense" page.
        2.  Enter description.
        3.  For "Amount", enter `10`.
        4.  Select "USD" from the "Currency" dropdown.
        5.  Enter a valid transaction date.
        6.  Click "Register Expense".
    *   *Expected Result:*
        *   Transaction is saved successfully.
        *   In the database: `original_amount` is `10.00`, `currency` is `"USD"`.
        *   `exchange_rate_usd` is populated (e.g., `1200.0000` if default from service for the given date).
        *   `amount` (ARS value) is calculated correctly (e.g., `10.00 * 1200.0000 = 12000.00`).

4.  **Editing Transaction:**
    *   **Test Case 4.1 (ARS to USD):**
        1.  Create and save an ARS transaction (e.g., Original Amount: 1200 ARS, Date: D1, Rate on D1: R1=1200). DB: `original_amount=1200`, `currency="ARS"`, `amount=1200`, `exchange_rate_usd=R1`.
        2.  Edit this transaction. Change "Currency" to "USD" (original amount field still shows 1200).
        3.  Save.
    *   *Expected Result:* `original_amount` remains `1200` (now interpreted as USD), `currency` is `"USD"`. `exchange_rate_usd` is R1 (or re-fetched if date changed). `amount` (ARS) is recalculated (e.g., `1200 * R1 = 1440000`).
    *   **Test Case 4.2 (USD to ARS):**
        1.  Create and save a USD transaction (e.g., Original Amount: 10 USD, Date: D1, Rate on D1: R1=1200). DB: `original_amount=10`, `currency="USD"`, `amount=12000`, `exchange_rate_usd=R1`.
        2.  Edit this transaction. Change "Currency" to "ARS" (original amount field still shows 10).
        3.  Save.
    *   *Expected Result:* `original_amount` remains `10` (now interpreted as ARS), `currency` is `"ARS"`. `exchange_rate_usd` is R1 (or re-fetched). `amount` (ARS) becomes `10.00`.
    *   **Test Case 4.3 (Change Original Amount - USD):**
        1.  Create and save a USD transaction (e.g., Original Amount: 10 USD, Date: D1, Rate on D1: R1=1200). DB: `amount=12000`.
        2.  Edit this transaction. Change "Amount" (original_amount) to `15`. Currency remains "USD".
        3.  Save.
    *   *Expected Result:* `original_amount` is `15.00`, `currency` is `"USD"`. `exchange_rate_usd` is R1. `amount` (ARS) is updated (e.g., `15 * R1 = 18000`).
    *   **Test Case 4.4 (Change Transaction Date - USD):**
        1.  Create and save a USD transaction (e.g., Original Amount: 10 USD, Date: D1, Rate on D1: R1=1200 from service). DB: `amount=12000`, `exchange_rate_usd=R1`.
        2.  Assume rate for Date D2 is R2=1300 (can be mocked in service or use different actual dates if API implemented).
        3.  Edit the transaction. Change "Transaction Date" to D2.
        4.  Save.
    *   *Expected Result:* `original_amount` is `10.00`, `currency` is `"USD"`. `exchange_rate_usd` is updated to R2. `amount` (ARS) is updated (e.g., `10 * R2 = 13000`).

5.  **Validation:**
    *   **Test Case 5.1:** In the transaction form, enter non-decimal characters (e.g., "abc") in the "Amount" (`original_amount`) field.
        *   *Expected Result:* Form shows a validation error for the amount field. Transaction is not saved.
    *   **Test Case 5.2:** (If applicable, depends on form field definition) Attempt to submit the form without selecting a currency.
        *   *Expected Result:* Form shows a validation error if "Currency" is a required field and not defaulted. Transaction is not saved. (Currently, `currency` model field has a default, so this might always be populated).

## IV. Display Logic

1.  **Transaction List (`accounting/transaction_list.html`):**
    *   **Test Case 1.1 (ARS Transaction):**
        1.  Create an ARS transaction: Original Amount = 250 ARS, Date = D1.
    *   *Expected Result on list view:*
        *   "Monto Original" column: "250.00 ARS".
        *   "Monto (ARS)" column: "250.00 ARS".
    *   **Test Case 1.2 (USD Transaction):**
        1.  Create a USD transaction: Original Amount = 15 USD, Date = D1. Assume exchange rate R1 = 1200.0000 for D1.
    *   *Expected Result on list view:*
        *   "Monto Original" column: "15.00 USD".
        *   "Monto (ARS)" column: "18000.00 ARS".

2.  **Dashboard (`dashboard/templates/dashboard/dashboard.html`):**
    *   **Test Case 2.1:**
        1.  Ensure a mix of ARS and USD transactions exist, with known ARS equivalent amounts.
        2.  Example:
            *   T1: 200 ARS (original_amount=200, currency=ARS, amount=200)
            *   T2: 10 USD (original_amount=10, currency=USD, exchange_rate_usd=1200, amount=12000)
    *   *Expected Result on dashboard's "Recent Expenses":*
        *   T1 is displayed as "200.00 ARS".
        *   T2 is displayed as "12000.00 ARS".
        *   All amounts are shown in ARS with the "ARS" indicator.

## V. Edge Cases/Error Handling

1.  **Exchange Rate Service Failure in View:**
    *   **Test Case 1.1:** Temporarily modify `get_usd_exchange_rate` to return `None` or raise an unexpected `Exception`. Attempt to create/edit a USD transaction.
    *   *Expected Result:* The view should handle this gracefully.
        *   Ideal: Transaction is not saved. An error message is displayed to the user (e.g., "Could not retrieve exchange rate. Please try again later."). The form might be re-rendered with existing data.
        *   Current implementation in views uses a `messages.warning` and a hardcoded fallback if `current_rate` is `None` (though the service aims to always return a default). Test this specific path to ensure the warning appears and calculation uses the hardcoded fallback.
        *   The goal is to prevent data corruption (e.g., `amount` being `None` or calculated incorrectly) and provide user feedback.

This testing plan will be used to verify the correct implementation and functionality of the multi-currency expense feature.
