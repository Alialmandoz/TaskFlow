## Expense Tracking (`accounting` app)

The `accounting` application is designed to help users manage their financial transactions, primarily focusing on expense tracking. It allows for categorization of expenses, association with projects, and leverages AI to streamline the process of recording expenditures.

### Core Data Models

The expense tracking system is built upon two key models defined in `accounting/models.py`:

1.  **`Category`**: Represents a user-defined category for classifying transactions.
    *   **Key Attributes**:
        *   `name` (CharField): The name of the category (e.g., "Food", "Transport", "Software").
        *   `user` (ForeignKey to `User`): Links the category to a specific user. Category names are unique per user, as enforced by `unique_together = ('name', 'user')`.

2.  **`Transaction`**: Represents an individual financial transaction, typically an expense.
    *   **Key Attributes**:
        *   `description` (CharField): A description of the transaction (e.g., "Lunch with client", "Monthly software subscription").
        *   `amount` (DecimalField): The monetary value of the transaction.
        *   `transaction_date` (DateField): The date on which the transaction occurred. Defaults to the current date.
        *   `type` (CharField): The type of transaction, with 'expense' as the current default and primary focus.
        *   `category` (ForeignKey to `Category`): Links the transaction to one of the user's predefined categories. This is optional.
        *   `project` (ForeignKey to `tasks.Project`): Optionally links the transaction to a project defined in the `tasks` application, enabling project-based cost tracking.
        *   `user` (ForeignKey to `User`): Links the transaction directly to the user who recorded it.
        *   `notes` (TextField): Optional field for any additional notes.
        *   `original_instruction` (TextField): Stores the original user instruction if the transaction data was initially extracted via an AI command, offering context for the entry.
        *   `created_at` (DateTimeField): Timestamp for when the transaction was recorded (auto-generated).
        *   `updated_at` (DateTimeField): Timestamp for the last update (auto-generated).

### Expense and Category Management

**1. Category Management:**

*   Categories are specific to each user. Users can define their own set of categories to organize their expenses.
*   The `TransactionForm` (in `accounting/forms.py`), used for manual transaction entry, dynamically populates its category selection field with categories belonging to the currently logged-in user.
*   While detailed views for category CRUD (Create, Read, Update, Delete) are not explicitly covered here, the system infrastructure supports user-owned categories (e.g., through Django admin or future dedicated views). The AI-assisted expense creation also includes functionality to create new categories on the fly if specified by the user.

**2. Manual Transaction Creation:**

*   Users can manually record new expenses using the `TransactionForm`. This form allows input for `description`, `amount`, `transaction_date`, `type` (defaulted to 'expense'), `category` (chosen from the user's list), associated `project` (chosen from the user's projects), and `notes`.
*   The `transaction_create` view (in `accounting/views.py`) handles the submission of this form. It automatically assigns the transaction to the logged-in `request.user`.

**3. AI-Assisted Expense Data Extraction & Confirmation:**

A key feature is the system's ability to process natural language instructions to extract expense information, facilitating quicker recording. This is primarily handled by the `ai_command_handler` view (located in `tasks/views.py` due to its shared nature).

*   **Information Extraction Process**:
    1.  User provides a natural language instruction (e.g., "Spent $25 on lunch yesterday for the marketing project" or "Record a $150 software purchase for 'Alpha Project' for today, categorize as 'Software'").
    2.  The `ai_command_handler` sends this instruction to the Google Gemini AI model. To improve accuracy, the instruction is augmented with context, including the current date and a list of the user's existing expense categories (fetched from `Category.objects.filter(user=request.user)`).
    3.  The AI is configured with an `extract_expense_data` function declaration. This function aims to identify and return:
        *   `description`: What the expense was for.
        *   `amount`: The monetary value.
        *   `transaction_date`: The date of the expense (resolving relative dates like "yesterday" based on the provided current date).
        *   `category_name_guess`: A suggestion for an existing category.
        *   `project_name_guess`: A suggestion for an existing project.
    4.  The AI's response, containing these extracted fields, is sent back to the `ai_command_handler`.

*   **User Confirmation Step**:
    1.  The backend does not immediately create the transaction. Instead, it returns a JSON response to the frontend with `action_needed: "confirm_expense"`.
    2.  This response includes the `extracted_data` from the AI and a list of the user's `user_categories` (ID and name).
    3.  The frontend then presents these details to the user, allowing them to:
        *   Verify and correct any AI-extracted information (description, amount, date).
        *   Select an existing category from their list.
        *   Type in a name for a new category if the desired one doesn't exist.
        *   Confirm or select the associated project.

*   **Transaction Creation (Post-Confirmation)**:
    1.  Once the user confirms (and potentially modifies) the details on the frontend, the data is sent back to the `ai_command_handler` (under the `action == 'confirm_creation'` block).
    2.  This data now includes `selected_category_id` (if an existing category was chosen) or `create_category_with_name` (if a new one was specified by the user), along with other expense details.
    3.  The `create_transaction_from_data` service function (in `accounting/services.py`) is then invoked. This service:
        *   Parses and validates the `description`, `amount`, and `transaction_date`.
        *   If `selected_category_id` is provided, it fetches the corresponding `Category` object.
        *   If `create_category_with_name` is provided, it uses `Category.objects.get_or_create()` (with a case-insensitive lookup on `name` for the given `user`) to either find an existing category or create a new one.
        *   If a `project_name` is provided, it attempts to find the user's project (case-insensitive).
        *   Finally, it creates and saves the `Transaction` object, storing the `original_instruction` (the initial natural language query) for reference.

### User and Project Association

*   **User Ownership**: Both `Category` and `Transaction` models have a direct `ForeignKey` to the `User` model. This ensures that users can only access and manage their own financial data. Views like `transaction_list` filter records by `request.user`. The `TransactionFilterForm` used in this list view also correctly populates its category dropdown with only the user's categories.
*   **Project Linking**: Transactions can be optionally linked to projects from the `tasks` app via the `project` ForeignKey on the `Transaction` model. This allows for financial tracking within the context of specific projects, providing a more granular view of project-related expenditures. The `TransactionForm` and the AI-assisted flow both support associating expenses with user-owned projects.

### Relevant Views and Forms

*   **Views**:
    *   `accounting/views.py`:
        *   `transaction_list`: Displays a paginated list of the logged-in user's expenses. It incorporates the `TransactionFilterForm` to allow filtering by category.
        *   `transaction_create`: Handles the form for manually creating new expense transactions.
    *   `tasks/views.py`:
        *   `ai_command_handler`: Manages the interaction with the AI for extracting expense data from natural language, and subsequently handles the confirmed data to create transactions using the `accounting.services.create_transaction_from_data` service.
*   **Forms (`accounting/forms.py`)**:
    *   `TransactionForm`: Used for manual creation and editing of transactions. It dynamically populates choice fields (like category and project) based on the user's data.
    *   `TransactionFilterForm`: Used in the `transaction_list` view to enable filtering of transactions, primarily by category. Its category field is also populated with user-specific categories.

These components collectively provide a comprehensive system for tracking expenses, with both manual and AI-assisted input methods, ensuring data is correctly associated with users and optionally with their projects.
