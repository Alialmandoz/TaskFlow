# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\services.py

from django.contrib.auth.models import User
from .models import Project, Task
from django.shortcuts import get_object_or_404
# from django.utils import timezone # No se usa directamente aquí ahora mismo
# from datetime import date

# --- MODIFICADO: create_project_for_user ---
def create_project_for_user(
    user_obj: User,
    name: str,
    description: str = None,
    original_instruction: str = None # <-- AÑADIDO parámetro
) -> Project:
    """
    Crea un nuevo objeto Project asociado a un usuario dado.
    """
    if not isinstance(user_obj, User):
        raise ValueError("Invalid user object provided.")
    if not name:
        raise ValueError("Project name cannot be empty.")

    project = Project(
        user=user_obj,
        name=name,
        description=description,
        original_instruction=original_instruction # <-- AÑADIDO asignación
    )
    project.save()

    print(f"DEBUG: Project '{name}' created for user {user_obj.username}. Instruction: '{original_instruction if original_instruction else 'N/A'}'")
    return project
# --- FIN MODIFICADO ---

# --- MODIFICADO: create_task_for_project ---
def create_task_for_project(
    project_obj: Project,
    description: str,
    status: str = 'todo',
    due_date=None,
    original_instruction: str = None # <-- AÑADIDO parámetro
) -> Task:
    """
    Crea un nuevo objeto Task asociado a un proyecto dado.
    """
    if not isinstance(project_obj, Project):
        raise ValueError("Invalid project object provided.")
    if not description:
        raise ValueError("Task description cannot be empty.")

    task = Task(
        project=project_obj,
        description=description,
        status=status,
        due_date=due_date,
        original_instruction=original_instruction # <-- AÑADIDO asignación
    )
    task.save()

    print(f"DEBUG: Task '{description[:20]}...' created for project '{project_obj.name}'. Instruction: '{original_instruction if original_instruction else 'N/A'}'")
    return task
# --- FIN MODIFICADO ---

def get_project_by_user_and_name(user_obj: User, project_name: str) -> Project:
     """
     Busca un proyecto por nombre para un usuario específico.
     Lanza Project.DoesNotExist o Project.MultipleObjectsReturned si no se encuentra o hay duplicados.
     """
     if not isinstance(user_obj, User):
         raise ValueError("Invalid user object provided.")
     if not project_name:
         raise ValueError("Project name cannot be empty for lookup.")
     return get_object_or_404(Project, user=user_obj, name=project_name)