# Manual Test Steps: Deletion from Dashboard

This document outlines the manual test steps for verifying the task and transaction deletion functionalities directly from the application's dashboard.

## 1. Testing Task Deletion from Dashboard:

a.  **Login**: Log in to the application with valid user credentials.
b.  **Prerequisites**: Ensure there is at least one project with a minimum of two tasks. If such data does not exist, create a project and add at least two tasks to it.
c.  **Navigate**: Go to the Dashboard page.
d.  **Identify Task**: In the "Mis Proyectos" section, locate a project and identify a specific task within that project that you intend to delete.
e.  **Initiate Deletion**: Click the 'Eliminar' (Delete) button associated with the chosen task.
f.  **Confirmation Dialog (Appearance)**:
    *   **Expected Result**: A JavaScript confirmation dialog should appear with the message: "Are you sure you want to delete this task?".
g.  **Cancel Deletion**: Click the 'Cancel' button on the confirmation dialog.
h.  **Verify Cancellation**:
    *   **Expected Result**: The task should remain visible on the dashboard within its project. No changes should occur.
i.  **Re-initiate Deletion**: Click the 'Eliminar' (Delete) button for the same task again.
j.  **Confirm Deletion**: Click 'OK' (or 'Confirm', 'Yes', depending on the browser's dialog) on the JavaScript confirmation dialog.
k.  **Verify Deletion on Dashboard**:
    *   **Expected Result**: The dashboard page should update. The specific task that was deleted should no longer be visible under its project on the dashboard. Other tasks within the same project (if any) should remain visible.
l.  **Navigate to Project Detail Page**: Navigate to the detail page for the project that contained the now-deleted task (e.g., by clicking the project's name).
m. **Verify Deletion on Project Detail Page**:
    *   **Expected Result**: The deleted task should also be absent from the task list on the project's detail page.

## 2. Testing Transaction Deletion from Dashboard:

a.  **Login**: Log in to the application with valid user credentials.
b.  **Prerequisites**: Ensure there are at least two recent transactions recorded for the user. If not, create them (e.g., using the AI console or manual entry). The dashboard typically shows the latest 5, so ensure the one to be deleted is visible.
c.  **Navigate**: Go to the Dashboard page.
d.  **Identify Transaction**: In the "Mis Gastos Recientes" (My Recent Expenses) section, identify a specific transaction you intend to delete.
e.  **Initiate Deletion**: Click the 'Eliminar' (Delete) button associated with that transaction.
f.  **Confirmation Dialog (Appearance)**:
    *   **Expected Result**: A JavaScript confirmation dialog should appear with the message: "Are you sure you want to delete this transaction?".
g.  **Cancel Deletion**: Click the 'Cancel' button on the confirmation dialog.
h.  **Verify Cancellation**:
    *   **Expected Result**: The transaction should remain visible in the "Mis Gastos Recientes" list on the dashboard. No changes should occur.
i.  **Re-initiate Deletion**: Click the 'Eliminar' (Delete) button for the same transaction again.
j.  **Confirm Deletion**: Click 'OK' (or 'Confirm', 'Yes') on the JavaScript confirmation dialog.
k.  **Verify Deletion on Dashboard**:
    *   **Expected Result**: The dashboard page should update. The specific transaction that was deleted should no longer be visible in the "Mis Gastos Recientes" list. If the user has more than five transactions overall, the list might repopulate with another transaction that was not previously visible, maintaining a list of up to five recent items.
l.  **Navigate to Transaction List Page**: Navigate to the main transaction list page (e.g., "Mis Gastos Registrados" or equivalent in the accounting section).
m. **Verify Deletion on Transaction List Page**:
    *   **Expected Result**: The deleted transaction should also be absent from the comprehensive list of transactions.
