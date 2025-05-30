# TaskFlow Project

## Overview

TaskFlow is a project designed to manage tasks and track expenses. It leverages the Django framework to provide a robust backend and a user-friendly interface. Key features include task management, expense tracking with multi-currency support, an interactive dashboard for visualizing project data, and AI integration for enhanced functionality.

## Project Report

The following sections provide detailed insights into the various aspects of the TaskFlow project:

| Section                                     | Link                                                                                      |
| :------------------------------------------ | :---------------------------------------------------------------------------------------- |
| Introduction                                | [Introduction](reports/report_introduction.md)                                           |
| Django Framework Usage                      | [Django Framework Usage](reports/django_framework_section.md)                            |
| Task Management (`tasks` app)               | [Task Management](reports/task_management_section.md)                                    |
| Expense Tracking (`accounting` app)         | [Expense Tracking](reports/expense_tracking_section.md)                                  |
| Dashboard (`dashboard` app)                 | [Dashboard](reports/dashboard_section.md)                                                |
| AI Integration with Google Gemini           | [AI Integration](reports/ai_integration_section.md)                                      |
| Database Design and Management              | [Database Design](reports/database_section.md)                                           |
| Testing - Multi Currency Test Plan          | [Multi Currency Test Plan](reports/multi_currency_test_plan.md)                          |
| Manual Tests - Dashboard Delete             | [Manual Tests - Dashboard Delete](reports/manual_dashboard_delete_tests.md)              |
| Manual Tests - Dashboard Edit Links         | [Manual Tests - Dashboard Edit Links](reports/manual_dashboard_edit_links_tests.md)        |
| Potential Enhancements                      | [Potential Enhancements](reports/potential_enhancements_section.md)                      |
| Conclusion                                  | [Conclusion](reports/conclusion_section.md)                                              |
| Full Project Report                         | [Full Project Report](reports/project_report.md)                                         |

## Getting Started

To get started with the TaskFlow project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd TaskFlowProject
    ```
2.  **Install dependencies:**
    Make sure you have Python and pip installed. Then, install the required packages using `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run migrations:**
    Apply the database migrations to set up your database schema:
    ```bash
    python manage.py migrate
    ```
4.  **Create a superuser (optional but recommended):**
    This will allow you to access the Django admin interface.
    ```bash
    python manage.py createsuperuser
    ```
5.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will typically be available at `http://127.0.0.1:8000/`.

This README provides a comprehensive starting point for understanding and running the TaskFlow project. For more detailed information, please refer to the linked report sections.
