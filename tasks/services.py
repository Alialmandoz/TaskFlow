# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\services.py

# Importamos los modelos necesarios
from django.contrib.auth.models import User
from .models import Project, Task

# Importamos get_object_or_404 o manejaremos la excepción directamente en la vista
# Para estas funciones de servicio, es mejor que lancen excepciones si algo falla,
# y la vista que las llama se encargará de manejar esas excepciones y responder al usuario.
from django.shortcuts import get_object_or_404 # Puede ser útil aquí si queremos que la función encuentre el proyecto

# Si vas a manejar fechas de vencimiento, podrías necesitar esto:
# from django.utils import timezone
# from datetime import date # O date para campos DateField

def create_project_for_user(user_obj: User, name: str, description: str = None) -> Project:
    """
    Crea un nuevo objeto Project asociado a un usuario dado.
    Lanza una excepción si el usuario no es un objeto User válido o si falta el nombre.
    """
    if not isinstance(user_obj, User):
        raise ValueError("Invalid user object provided.")
    if not name:
        raise ValueError("Project name cannot be empty.")

    # Creamos y guardamos la instancia del Project
    # Django asignará user y created_at automáticamente si los campos están configurados así
    project = Project(user=user_obj, name=name, description=description)
    project.save()

    # Devolvemos el objeto Project recién creado
    print(f"DEBUG: Project '{name}' created for user {user_obj.username}") # Log de depuración
    return project

def create_task_for_project(project_obj: Project, description: str, status: str = 'todo', due_date=None) -> Task:
    """
    Crea un nuevo objeto Task asociado a un proyecto dado.
    project_obj debe ser una instancia válida de Project.
    Lanza una excepción si el proyecto o la descripción no son válidos.
    """
    if not isinstance(project_obj, Project):
        raise ValueError("Invalid project object provided.")
    if not description:
        raise ValueError("Task description cannot be empty.")

    # Puedes añadir validación básica para status si quieres,
    # aunque el modelo ya tiene choices y default.
    # if status not in [choice[0] for choice in Task.STATUS_CHOICES]:
    #     status = 'todo' # O lanzar un error

    # Puedes intentar parsear la fecha si due_date no es un objeto date/None
    # if due_date and not isinstance(due_date, date):
    #     try:
    #         # Implementar lógica para parsear la fecha si viene como string,
    #         # dependiendo de cómo la API de Gemini la devuelva.
    #         # Por ahora, asumimos que due_date es None o un objeto date válido.
    #         pass # Aquí iría la lógica de parseo de fecha
    #     except ValueError:
    #         due_date = None # O lanzar un error indicando fecha inválida


    # Creamos y guardamos la instancia de la Task
    task = Task(project=project_obj, description=description, status=status, due_date=due_date)
    task.save()

    # Devolvemos el objeto Task recién creado
    print(f"DEBUG: Task '{description[:20]}...' created for project '{project_obj.name}'") # Log de depuración
    return task

# Opcional: Una función para encontrar un proyecto por nombre y usuario (será llamada por la vista, no directamente por Gemini)
def get_project_by_user_and_name(user_obj: User, project_name: str) -> Project:
     """
     Busca un proyecto por nombre para un usuario específico.
     Lanza Project.DoesNotExist o Project.MultipleObjectsReturned si no se encuentra o hay duplicados.
     """
     if not isinstance(user_obj, User):
         raise ValueError("Invalid user object provided.")
     if not project_name:
         raise ValueError("Project name cannot be empty for lookup.")

     # Usamos get_object_or_404 (aunque el nombre es get_object_or_404, aquí lanza DoesNotExist/MultipleObjectsReturned)
     # Filtramos por usuario Y nombre
     return get_object_or_404(Project, user=user_obj, name=project_name)