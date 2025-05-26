## Task Management (`tasks` app)

The `tasks` application is the cornerstone of the TaskFlow system, providing robust functionalities for managing projects and individual tasks. It allows users to organize their work effectively, track progress, and leverage AI for streamlined task creation.

### Core Data Models

The task management system relies on two primary data models defined in `tasks/models.py`:

1.  **`Project`**: Represents a container for tasks, helping to group related activities.
    *   **Key Attributes**:
        *   `name` (CharField): The name of the project.
        *   `description` (TextField): An optional detailed description of the project.
        *   `user` (ForeignKey to `User`): Links the project to a specific user, ensuring data privacy and ownership.
        *   `created_at` (DateTimeField): Timestamp for when the project was created (auto-generated).
        *   `original_instruction` (TextField): Stores the original user instruction if the project was created via an AI command, providing context and transparency.

2.  **`Task`**: Represents an individual action item or to-do within a project.
    *   **Key Attributes**:
        *   `description` (TextField): A detailed description of the task.
        *   `status` (CharField): Tracks the current state of the task. It uses predefined choices: 'todo' (Por hacer), 'doing' (En progreso), and 'done' (Completada). The default status upon creation is 'todo'.
        *   `project` (ForeignKey to `Project`): Links the task to its parent project.
        *   `created_at` (DateTimeField): Timestamp for when the task was created (auto-generated).
        *   `due_date` (DateField): An optional date by which the task should be completed.
        *   `completed_at` (DateTimeField): Timestamp for when the task was marked as completed. This is updated by model methods.
        *   `original_instruction` (TextField): Stores the original user instruction if the task was created via an AI command.

User association is primarily managed at the `Project` level. Tasks are implicitly associated with the user who owns the parent project.

### Project and Task Creation

The system supports both manual and AI-assisted creation of projects and tasks:

**1. Manual Creation:**

*   **Projects**: Users can create projects manually using a dedicated form (`ProjectForm` from `tasks/forms.py`), which captures the `name` and `description`. The `project_create` view (in `tasks/views.py`) handles form submission, automatically associating the new project with the logged-in `request.user`.
*   **Tasks**: Within a project, users can add tasks using the `TaskForm` (from `tasks/forms.py`). This form collects the `description`, initial `status`, and an optional `due_date`. The `task_create` view (in `tasks/views.py`), which is accessed via a project-specific URL, handles task creation and links it to the correct project.

**2. AI-Assisted Creation:**

A significant feature is the ability to create projects and tasks using natural language instructions through the `ai_command_handler` view (in `tasks/views.py`). This view processes user input by leveraging the Google Gemini AI model.

*   **Process**:
    1.  User provides an instruction (e.g., "Create a project for my new website" or "Add a task to 'Website Project' to design the homepage by next Friday").
    2.  The `ai_command_handler` sends this instruction, along with contextual information (like current date and existing user categories for disambiguation if needed), to the Gemini model.
    3.  The AI model is configured with specific function declarations (`GEMINI_FUNCTION_DECLARATIONS` in `tasks/views.py`) that allow it to understand the intent to create a project or task. These declarations include:
        *   `create_project`: Expects parameters like `name` and `description`.
        *   `create_task`: Expects parameters like `project_name`, `description`, `status`, and `due_date`.
    4.  If the AI identifies an intent to create, it returns a function call request with the extracted parameters.
    5.  The backend then uses dedicated service functions (e.g., `create_project_for_user`, `create_task_for_project` from `tasks/services.py`) to create the actual database entries.
    6.  The `original_instruction` field in both `Project` and `Task` models is populated with the user's raw text input for traceability.

This AI integration simplifies the creation process, allowing users to quickly populate their task lists without navigating multiple forms.

### Status Tracking

Task progress is managed via the `status` attribute in the `Task` model.

*   The available statuses are 'todo', 'doing', and 'done'.
*   Tasks are created with a default status of 'todo'.
*   The `Task` model includes helper methods:
    *   `mark_as_completed()`: Changes the task's status to 'done' and sets the `completed_at` timestamp to the current time.
    *   `mark_as_todo()`: Can be used to revert a 'done' task back to 'todo', clearing the `completed_at` timestamp.

These statuses and methods allow for clear tracking of task completion.

### User Association and Access Control

*   Each `Project` is directly linked to a `User` via a `ForeignKey`.
*   `Task` entities are associated with a `Project`. Therefore, a task belongs to the user who owns the project.
*   Views responsible for displaying projects and tasks, such as `project_list` and `project_detail` (defined in `tasks/views.py`), ensure that users can only see and interact with their own data by filtering querysets based on `request.user`.

### Relevant Views and Forms

*   **Views (`tasks/views.py`)**:
    *   `project_list`: Displays all projects belonging to the logged-in user.
    *   `project_detail`: Shows the details of a specific project and lists its associated tasks.
    *   `project_create`: Handles the manual creation of new projects.
    *   `task_create`: Handles the manual creation of new tasks within a project.
    *   `ai_command_handler`: Processes natural language commands for AI-assisted creation.
*   **Forms (`tasks/forms.py`)**:
    *   `ProjectForm`: Used for manual project creation, capturing `name` and `description`.
    *   `TaskForm`: Used for manual task creation, capturing `description`, `status`, and `due_date`.

These components work together to provide a comprehensive task management experience within the `tasks` application.
