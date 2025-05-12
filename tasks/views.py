# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse # Para devolver respuestas JSON
from django.views.decorators.csrf import csrf_exempt # Para deshabilitar CSRF si se prueba con herramientas externas (ver nota)
from django.views.decorators.http import require_POST # Para asegurar que solo sea POST
import json # Para parsear el cuerpo de la solicitud JSON
import os # Para obtener la clave de API

# Importaciones de Gemini
import google.generativeai as genai # Importa la biblioteca de Gemini
from google.generativeai.types import HarmCategory, HarmBlockThreshold # Para configurar seguridad

from .models import Project, Task
from .forms import ProjectForm, TaskForm
# Importamos nuestras funciones de servicio
from .services import create_project_for_user, create_task_for_project, get_project_by_user_and_name

# Decorador para asegurar que solo usuarios autenticados puedan acceder a estas vistas.
# tasks/views.py - extracto de la vista project_list actualizada

@login_required
def project_list(request):
    """
    Vista para listar todos los proyectos pertenecientes al usuario autenticado,
    incluyendo sus tareas precargadas para eficiencia.
    """
    # Usamos prefetch_related para obtener todas las tareas asociadas
    # a los proyectos en una consulta adicional eficiente, en lugar de una por proyecto.
    projects = Project.objects.filter(user=request.user).prefetch_related('task_set').order_by('name')
    context = {
        'projects': projects
        # 'ai_console_url_name': 'tasks:ai_command_handler' # Ya no es necesario si el form está aquí
    }
    return render(request, 'tasks/project_list.html', context)

@login_required
def project_detail(request, pk):
    """
    Vista para mostrar los detalles de un proyecto específico y sus tareas asociadas.
    Solo muestra proyectos que pertenecen al usuario autenticado.
    """
    project = get_object_or_404(Project, pk=pk, user=request.user)
    tasks = project.task_set.all().order_by('due_date', 'created_at')
    context = {
        'project': project,
        'tasks': tasks
    }
    return render(request, 'tasks/project_detail.html', context)

@login_required
def project_create(request):
    """
    Vista para manejar la creación de nuevos proyectos.
    Responde a GET mostrando el formulario y a POST procesando los datos.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('tasks:project_list')
    else:
        form = ProjectForm()

    return render(request, 'tasks/project_form.html', {'form': form})

@login_required
def task_create(request, project_pk):
    """
    Vista para manejar la creación de nuevas tareas dentro de un proyecto específico.
    """
    project = get_object_or_404(Project, pk=project_pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('tasks:project_detail', pk=project.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'project': project})


# Definición de las funciones para Gemini
GEMINI_FUNCTION_DECLARATIONS = [
    {
        "name": "create_project",
        "description": "Crea un nuevo proyecto para el usuario. Útil cuando el usuario quiere iniciar un nuevo proyecto, plan o contenedor de tareas.",
        "parameters": {
            "type": "OBJECT", # Indica que los parámetros son un objeto con propiedades
            "properties": {
                "name": {
                    "type": "STRING",
                    "description": "El nombre del proyecto."
                },
                "description": {
                    "type": "STRING",
                    "description": "Una descripción detallada del proyecto (opcional)."
                }
            },
            "required": ["name"] # Indica qué propiedades son obligatorias
        }
    },
    {
        "name": "create_task",
        "description": "Crea una nueva tarea y la asigna a un proyecto existente del usuario. Útil cuando el usuario quiere añadir una nueva tarea, ítem por hacer, o acción a un proyecto.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "project_name": {
                    "type": "STRING",
                    "description": "El nombre del proyecto al que pertenece la tarea."
                },
                "description": {
                    "type": "STRING",
                    "description": "La descripción de la tarea a realizar."
                },
                "status": {
                    "type": "STRING",
                    "description": "El estado actual de la tarea. Valores permitidos: 'todo', 'doing', 'done'. Por defecto es 'todo' si no se especifica.",
                    "enum": ["todo", "doing", "done"] # Ayuda a Gemini a restringir los valores
                },
                "due_date": {
                    "type": "STRING",
                    "description": "La fecha de vencimiento de la tarea en formato AAAA-MM-DD (opcional)."
                }
            },
            "required": ["project_name", "description"]
        }
    }
]

# Nota sobre CSRF:
# Si vas a probar este endpoint desde una herramienta externa (como Postman)
# que no envía automáticamente el token CSRF, puedes usar @csrf_exempt temporalmente.
# Para un frontend web con JavaScript, asegúrate de incluir el token CSRF en tus solicitudes AJAX.
# @csrf_exempt # Descomentar SOLO para pruebas con herramientas externas si es necesario.


@login_required # Asegura que el usuario esté autenticado
@require_POST # Asegura que este endpoint solo acepte solicitudes POST
def ai_command_handler(request):
    try:
        # 1. Obtener la clave de API de forma segura
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("ERROR: GOOGLE_API_KEY no encontrada en el entorno.")
            return JsonResponse({'error': 'API Key no configurada en el servidor.'}, status=500)
        genai.configure(api_key=api_key)

        # 2. Parsear la instrucción del usuario desde el cuerpo de la solicitud JSON
        try:
            data = json.loads(request.body)
            user_instruction = data.get('instruction')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Cuerpo de la solicitud JSON inválido o vacío.'}, status=400)


        if not user_instruction:
            return JsonResponse({'error': 'Instrucción no proporcionada.'}, status=400)

        # 3. Preparar el modelo Gemini con las herramientas (nuestras funciones)
        # Consulta la documentación de Gemini para el nombre exacto del modelo recomendado.
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest', # O 'gemini-1.0-pro', etc.
            tools=GEMINI_FUNCTION_DECLARATIONS,
            safety_settings={ # Configuración de seguridad básica
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        # Iniciamos una sesión de chat. enable_automatic_function_calling=False para control manual.
        chat = model.start_chat(enable_automatic_function_calling=False)

        # 4. Enviar la instrucción del usuario a Gemini
        print(f"DEBUG: [AI Handler] Enviando a Gemini: '{user_instruction}' para el usuario {request.user.username}")
        response = chat.send_message(user_instruction)
        
        # 5. Procesar la respuesta de Gemini para llamadas a función
        # Accedemos a la primera parte del primer candidato (puede haber varios candidatos)
        if not response.candidates or not response.candidates[0].content.parts:
            print(f"DEBUG: [AI Handler] Respuesta de Gemini inesperada o vacía: {response.prompt_feedback}")
            # Si el prompt fue bloqueado, prompt_feedback puede dar información.
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                 return JsonResponse({'error': f'La instrucción fue bloqueada por seguridad: {response.prompt_feedback.block_reason_message}'}, status=400)
            return JsonResponse({'message': response.text if hasattr(response, 'text') else 'No se pudo obtener una respuesta clara de la IA.'})

        # Intentar acceder a function_call
        try:
            function_call_part = response.candidates[0].content.parts[0]
            if hasattr(function_call_part, 'function_call'):
                function_call = function_call_part.function_call
            else:
                function_call = None # No es una llamada a función
        except IndexError:
             print(f"DEBUG: [AI Handler] No se encontraron 'parts' en la respuesta de Gemini.")
             return JsonResponse({'message': response.text if hasattr(response, 'text') else 'Respuesta de IA sin partes procesables.'})


        if function_call:
            function_name = function_call.name
            args = function_call.args
            args_dict = {key: value for key, value in args.items()}

            print(f"DEBUG: [AI Handler] Gemini quiere llamar a '{function_name}' con args: {args_dict}")

            if function_name == "create_project":
                project_name = args_dict.get("name")
                description = args_dict.get("description") # Puede ser None
                if not project_name:
                    # (Opcional) Aquí podrías volver a llamar a Gemini pidiendo el nombre
                    return JsonResponse({'error': "Gemini no proporcionó un nombre para el proyecto."}, status=400)
                
                try:
                    project = create_project_for_user(request.user, project_name, description)
                    final_user_message = f"Proyecto '{project.name}' creado exitosamente."
                    print(f"INFO: [AI Handler] {final_user_message}")
                    return JsonResponse({'message': final_user_message, 'project_id': project.id, 'type': 'project_created'})
                except ValueError as e:
                    print(f"ERROR: [AI Handler] Error al crear proyecto: {str(e)}")
                    return JsonResponse({'error': f"Error al crear proyecto: {str(e)}"}, status=400)

            elif function_name == "create_task":
                project_name_for_task = args_dict.get("project_name")
                task_description = args_dict.get("description")
                status = args_dict.get("status", "todo") 
                due_date_str = args_dict.get("due_date")

                if not project_name_for_task or not task_description:
                    return JsonResponse({'error': "Gemini no proporcionó nombre de proyecto o descripción de tarea."}, status=400)

                try:
                    project_obj = get_project_by_user_and_name(request.user, project_name_for_task)
                    
                    parsed_due_date = None
                    if due_date_str:
                        try:
                            from datetime import datetime # Importación local
                            parsed_due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        except ValueError:
                            print(f"WARN: [AI Handler] Formato de fecha inválido '{due_date_str}' recibido de Gemini. Se ignorará la fecha.")
                            # Podrías informar al usuario que la fecha no se pudo parsear
                            # O intentar preguntarle de nuevo a Gemini por una fecha válida.
                            pass # Se usará None

                    task = create_task_for_project(project_obj, task_description, status, parsed_due_date)
                    final_user_message = f"Tarea '{task.description[:30]}...' añadida al proyecto '{project_obj.name}'."
                    print(f"INFO: [AI Handler] {final_user_message}")
                    return JsonResponse({'message': final_user_message, 'task_id': task.id, 'type': 'task_created'})
                except Project.DoesNotExist:
                    print(f"WARN: [AI Handler] Proyecto '{project_name_for_task}' no encontrado para {request.user.username}.")
                    return JsonResponse({'error': f"El proyecto '{project_name_for_task}' no fue encontrado. ¿Quizás quisiste decir otro nombre o necesitas crearlo primero?"}, status=404)
                except ValueError as e:
                    print(f"ERROR: [AI Handler] Error al crear tarea: {str(e)}")
                    return JsonResponse({'error': f"Error al crear tarea: {str(e)}"}, status=400)
            
            else:
                print(f"WARN: [AI Handler] Función desconocida solicitada por Gemini: {function_name}")
                return JsonResponse({'error': f"Función desconocida solicitada por Gemini: {function_name}"}, status=400)
        else:
            # Si Gemini no devuelve una llamada a función, devolvemos su texto.
            print(f"DEBUG: [AI Handler] Gemini respondió con texto: '{response.text if hasattr(response, 'text') else 'Respuesta vacía'}'")
            return JsonResponse({'message': response.text if hasattr(response, 'text') else 'La IA no sugirió una acción específica.'})

    except Exception as e:
        # Captura general de errores para depuración
        import traceback # Para obtener más detalles del error
        print(f"CRITICAL ERROR en ai_command_handler: {type(e).__name__} - {str(e)}")
        print(traceback.format_exc()) # Imprime el stack trace completo del error
        return JsonResponse({'error': 'Ocurrió un error inesperado y crítico en el servidor.'}, status=500)
    
