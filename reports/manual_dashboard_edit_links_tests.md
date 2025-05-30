# Manual Test Steps: 'Edit' Links from Dashboard

This document outlines the manual test steps for verifying the functionality of the 'Edit' links for tasks and transactions directly from the application's dashboard.

## 1. Testing 'Edit Task' Links from Dashboard:

a.  **Login**: Log in to the application with valid user credentials.
b.  **Prerequisites**: Ensure there is at least one project with at least one task. If not, create them (e.g., using the AI console or manual project/task creation).
c.  **Navigate**: Go to the Dashboard page.
d.  **Identify Task**: In the "Mis Proyectos" (My Projects) section, locate a project and identify a specific task listed under it.
e.  **Click Edit Link**: Click the 'Editar' (Edit) button/link associated with the chosen task on the dashboard.
f.  **Verify Navigation and Form Pre-fill**:
    *   **Expected Result**: You should be navigated to the 'Edit Task' page.
        *   The URL should match the pattern `/tasks/<task_pk>/edit/` (where `<task_pk>` is the ID of the task).
        *   The form on the page should be pre-filled with the current details of the selected task (e.g., description, status, due date).
        *   The page title should indicate "Edit Task" and correctly reference the task's parent project (e.g., "Edit Task for Project: 'Project Name'").
g.  **Modify Task Details**: Make a small, valid change to one of the task's fields (e.g., slightly alter the description or change its status).
h.  **Save Changes**: Click the 'Save Changes' (or equivalent) button on the edit form.
i.  **Verify Redirection and Update on Project Detail Page**:
    *   **Expected Result**: The task should be updated successfully.
        *   You should be redirected to the project detail page (`/tasks/projects/<project_pk>/`).
        *   The updated task information (e.g., the new description or status) should be visible on this page.
j.  **Verify Update on Dashboard**: Navigate back to the Dashboard.
    *   **Expected Result**: If the edited task is still visible on the dashboard (e.g., its description change didn't alter its sort order out of view or its status is still relevant for display), the updated information should be reflected there.

## 2. Testing 'Edit Transaction' Links from Dashboard:

a.  **Login**: Log in to the application with valid user credentials.
b.  **Prerequisites**: Ensure there is at least one recent transaction recorded for the user that appears in the "Mis Gastos Recientes" (My Recent Expenses) list on the dashboard. If not, create a new transaction.
c.  **Navigate**: Go to the Dashboard page.
d.  **Identify Transaction**: In the "Mis Gastos Recientes" section, identify a specific transaction.
e.  **Click Edit Link**: Click the 'Editar' (Edit) button/link associated with that transaction on the dashboard.
f.  **Verify Navigation and Form Pre-fill**:
    *   **Expected Result**: You should be navigated to the 'Edit Transaction' page.
        *   The URL should match the pattern `/accounting/transaction/<transaction_pk>/edit/` (where `<transaction_pk>` is the ID of the transaction).
        *   The form on the page should be pre-filled with the current details of the selected transaction (e.g., description, amount, date, category, associated project, notes).
        *   The page title should indicate "Edit Transaction".
g.  **Modify Transaction Details**: Make a small, valid change to one of the transaction's fields (e.g., update the notes, slightly change the amount, or re-assign the category).
h.  **Save Changes**: Click the 'Save Changes' (or equivalent) button on the edit form.
i.  **Verify Redirection and Update on Transaction List Page**:
    *   **Expected Result**: The transaction should be updated successfully.
        *   You should be redirected to the main transaction list page (`/accounting/transactions/`).
        *   The updated transaction information should be visible in the list, reflecting the changes made.
j.  **Verify Update on Dashboard**: Navigate back to the Dashboard.
    *   **Expected Result**: If the edited transaction is still among the most recent ones displayed on the dashboard, its updated information (e.g., new description or amount) should be reflected there.
