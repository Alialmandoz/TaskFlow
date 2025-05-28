## Database Design and Management

The database serves as the persistent storage layer for all data within the TaskFlow application, including user information, projects, tasks, expense categories, and financial transactions. Django's powerful Object-Relational Mapper (ORM) is utilized for all interactions with the database, providing an abstraction layer over direct SQL.

### Core Data Models

The application's data is organized into several key models, defined within their respective apps:

**1. `tasks.models`:**

*   **`Project`**: Represents a user-defined project or a container for tasks.
    *   Key attributes: `name` (CharField), `description` (TextField, optional), `user` (ForeignKey to `User`), `created_at` (DateTimeField, auto-added), `original_instruction` (TextField, for AI-created projects).
*   **`Task`**: Represents an individual task or to-do item within a `Project`.
    *   Key attributes: `description` (TextField), `status` (CharField with choices: 'todo', 'doing', 'done'), `project` (ForeignKey to `Project`), `created_at` (DateTimeField, auto-added), `due_date` (DateField, optional), `completed_at` (DateTimeField, optional), `original_instruction` (TextField, for AI-created tasks).

**2. `accounting.models`:**

*   **`Category`**: Defines user-specific categories for organizing expenses.
    *   Key attributes: `name` (CharField), `user` (ForeignKey to `User`). Importantly, `Meta.unique_together = ('name', 'user')` ensures that category names are unique per user.
*   **`Transaction`**: Records individual financial transactions, primarily expenses.
    *   Key attributes: `description` (CharField), `amount` (DecimalField), `transaction_date` (DateField), `type` (CharField, default 'expense'), `category` (ForeignKey to `Category`, nullable), `project` (ForeignKey to `tasks.Project`, nullable), `user` (ForeignKey to `User`), `notes` (TextField, optional), `original_instruction` (TextField, for AI-processed expenses), `created_at` (DateTimeField, auto-added), `updated_at` (DateTimeField, auto-updated).

### Key Relationships

These models are interconnected through various relationships, primarily using Django's `ForeignKey` field:

*   **User Ownership**: All primary data entities (`Project`, `Category`, `Transaction`) are directly linked to the `User` model (from `django.contrib.auth.models`). `Task` models are indirectly linked to a `User` via their parent `Project`. This ensures data isolation and user-specific views.
*   **Project-Task Relationship**: A one-to-many relationship exists between `Project` and `Task`. A single project can have multiple tasks. The `on_delete=models.CASCADE` setting on `Task.project` ensures that if a project is deleted, all its associated tasks are also deleted.
*   **Transaction-Category Relationship**: A many-to-one relationship exists where a `Transaction` can belong to one `Category`. If a `Category` is deleted, the `category` field in related `Transaction` instances is set to `NULL` due to `on_delete=models.SET_NULL`.
*   **Transaction-Project Relationship**: A `Transaction` can optionally be associated with a `Project`. This is also a many-to-one relationship with `on_delete=models.SET_NULL`, allowing transactions to remain even if the linked project is removed.

### Django Object-Relational Mapper (ORM)

All interactions with the underlying database (e.g., SQLite, PostgreSQL) are managed through Django's ORM.
*   **Model-to-Table Mapping**: Each model class (e.g., `Project`, `Task`) is mapped by the ORM to a corresponding table in the database. Fields in the model become columns in the table.
*   **Pythonic Database Operations**: Instead of writing raw SQL queries, database operations are performed using Python code. For example:
    *   Creating a new project: `Project.objects.create(name="New Project", user=request.user)`
    *   Querying tasks: `Task.objects.filter(project=my_project, status='todo')`
    *   Updating a task: `task.status = 'done'; task.save()`
*   **Benefits**:
    *   **Abstraction**: Hides the complexity of database-specific SQL syntax.
    *   **Productivity**: Speeds up development by allowing developers to work with Python objects.
    *   **Security**: Helps prevent SQL injection vulnerabilities by automatically escaping query parameters.
    *   **Portability**: Makes it easier to switch between different database systems with minimal code changes.

### Database Migrations

Django's migration system is used to manage and apply changes to the database schema as the application's models evolve over time.
*   **`migrations` Directory**: Each app (`tasks`, `accounting`) contains a `migrations` directory that stores migration files. These files are Python scripts that describe the changes to be made to the database schema (e.g., creating a table, adding a column, altering a field).
*   **Generating Migrations**: When changes are made to `models.py` (e.g., adding a new field or model), the `python manage.py makemigrations <app_name>` command is run. Django detects these changes and generates a new migration file.
*   **Applying Migrations**: The `python manage.py migrate` command applies any pending migrations to the database, updating the schema to match the current model definitions.
*   **Benefits**:
    *   **Version Control for Schema**: Database schema changes are tracked in version control alongside the codebase.
    *   **Reliable Updates**: Ensures that schema changes are applied consistently across different development, testing, and production environments.
    *   **Schema Evolution**: Facilitates the evolution of the database schema as application requirements change.

This structured approach to database design and management, powered by Django's ORM and migration system, provides a robust and maintainable foundation for the TaskFlow application.
