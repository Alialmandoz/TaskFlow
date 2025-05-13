# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import os
from datetime import datetime
import traceback

# Importaciones de Gemini
import google.generativeai as genai
# --- AÑADIDO: Importar excepción específica de Gemini ---
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException

# Modelos de Tasks
from .models import Project, Task
# Formularios de Tasks
from .forms import ProjectForm, TaskForm
# Servicios de Tasks
from .services import create_project_for_user, create_task_for_project, get_project_by_user_and_name

# Importaciones de Accounting
from accounting.models import Category, Transaction
from accounting.services import create_transaction_from_data


# Vista project_list simplificada (solo lista proyectos)
@login_required
def project_list(request):
    """
    Vista para listar SOLAMENTE los proyectos del usuario.
    El dashboard principal ahora está en la app 'dashboard'.
    """
    projects = Project.objects.filter(user=request.user).prefetch_related('task_set').order_by('name')
    context = {
        'projects': projects,
    }
    return render(request, 'tasks/project_list.html', context)

# Vistas de detalle, creación manual de proyecto y tarea (sin cambios)
@login_required
def project_detail(request, pk):
    """
    Vista para mostrar los detalles de un proyecto específico y sus tareas asociadas.
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
    Vista para manejar la creación manual de nuevos proyectos.
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
    Vista para manejar la creación manual de nuevas tareas dentro de un proyecto específico.
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

# Declaraciones de funciones Gemini (sin cambios)
GEMINI_FUNCTION_DECLARATIONS = [
     {
        "name": "create_project",
        "description": "Crea un nuevo proyecto para el usuario. Útil cuando el usuario quiere iniciar un nuevo proyecto, plan o contenedor de tareas.",
        "parameters": { "type": "OBJECT", "properties": { "name": { "type": "STRING", "description": "El nombre del proyecto." }, "description": { "type": "STRING", "description": "Una descripción detallada del proyecto (opcional)." } }, "required": ["name"] }
    },
    {
        "name": "create_task",
        "description": "Crea una nueva tarea y la asigna a un proyecto existente del usuario. Útil cuando el usuario quiere añadir una nueva tarea, ítem por hacer, o acción a un proyecto.",
        "parameters": { "type": "OBJECT", "properties": { "project_name": { "type": "STRING", "description": "El nombre del proyecto existente al que pertenece la tarea." }, "description": { "type": "STRING", "description": "La descripción de la tarea a realizar." }, "status": { "type": "STRING", "description": "El estado actual de la tarea. Valores permitidos: 'todo', 'doing', 'done'. Por defecto es 'todo' si no se especifica.", "enum": ["todo", "doing", "done"] }, "due_date": { "type": "STRING", "description": "La fecha de vencimiento de la tarea en formato AAAA-MM-DD (opcional)." } }, "required": ["project_name", "description"] }
    },
    {
        "name": "extract_expense_data",
        "description": "Extrae la información detallada de un gasto o transacción financiera a partir de la instrucción del usuario. El objetivo es recopilar los detalles para una posterior confirmación antes de registrar el gasto.",
        "parameters": { "type": "OBJECT", "properties": { "description": { "type": "STRING", "description": "La descripción detallada del gasto (ej. 'Almuerzo con cliente X', 'Compra de licencia de software Y')." }, "amount": { "type": "NUMBER", "description": "El monto numérico del gasto (ej. 25.50, 100)." }, "transaction_date": { "type": "STRING", "description": "La fecha en que se realizó el gasto, en formato AAAA-MM-DD (ej. '2024-07-15'). Si el usuario no especifica una fecha, no incluyas este campo o déjalo vacío." }, "category_name_guess": { "type": "STRING", "description": "El nombre de una categoría DE GASTOS *existente* a la que este gasto podría pertenecer (ej. 'Comida', 'Transporte', 'Software'). Si no estás seguro o el usuario no lo menciona, omite este campo." }, "project_name_guess": { "type": "STRING", "description": "El nombre de un proyecto *existente* al que este gasto podría estar asociado. Si el usuario no menciona un proyecto o si el gasto parece personal, omite este campo." } }, "required": ["description", "amount"] }
    }
]

# Vista del manejador de comandos IA
@login_required
@require_POST
def ai_command_handler(request):
    # --- MODIFICADO: Añadido bloque try...except principal para capturar errores de Gemini ---
    try:
        # 1. Configurar API Key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("ERROR: GOOGLE_API_KEY no encontrada.")
            return JsonResponse({'error': 'API Key no configurada.'}, status=500)
        genai.configure(api_key=api_key)

        # 2. Parsear JSON y determinar acción
        try:
            data = json.loads(request.body)
            action = data.get('action')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)

        # Manejo de la acción de confirmación (para gastos)
        if action == 'confirm_creation':
            confirmed_data = data.get('confirmed_data')
            if not confirmed_data:
                 return JsonResponse({'error': 'Datos de confirmación no proporcionados.'}, status=400)

            print(f"DEBUG: [AI Handler] Recibida confirmación con datos: {confirmed_data}")

            try:
                # Llamar al servicio de accounting para crear la transacción
                transaction = create_transaction_from_data(
                    user=request.user,
                    description=confirmed_data.get('description'),
                    amount=confirmed_data.get('amount'),
                    transaction_date_str=confirmed_data.get('transaction_date'),
                    category_name=confirmed_data.get('category_name'),
                    project_name=confirmed_data.get('project_name')
                )
                # Éxito al crear
                return JsonResponse({
                    'message': f"Gasto '{transaction.description[:30]}...' registrado exitosamente.",
                    'transaction_id': transaction.id,
                    'type': 'transaction_created'
                    })
            except (ValueError, TypeError) as e:
                print(f"ERROR: [AI Handler] Error al crear transacción: {str(e)}")
                return JsonResponse({'error': f"Error al registrar el gasto: {str(e)}"}, status=400)

        # Si no es confirmación, procesar instrucción normal
        user_instruction = data.get('instruction')
        if not user_instruction:
             return JsonResponse({'error': 'Instrucción no proporcionada.'}, status=400)

        # 3. Preparar y llamar a Gemini
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            tools=GEMINI_FUNCTION_DECLARATIONS,
            safety_settings={
                 HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                 HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                 HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                 HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        chat = model.start_chat(enable_automatic_function_calling=False)
        print(f"DEBUG: [AI Handler] Enviando a Gemini: '{user_instruction}' para {request.user.username}")

        # --- Llamada a Gemini ahora dentro del try principal ---
        response = chat.send_message(user_instruction)

        # 4. Procesar respuesta de Gemini (si no hubo excepción en send_message)
        # (La lógica de procesamiento se mueve dentro del try general)
        if not response.candidates or not response.candidates[0].content.parts:
            print(f"DEBUG: [AI Handler] Respuesta Gemini inesperada: {response.prompt_feedback}")
            # Manejar bloqueo por seguridad aquí si es necesario, aunque StopCandidateException lo hará
            if response.prompt_feedback and response.prompt_feedback.block_reason == 'SAFETY':
                 return JsonResponse({'error': 'La instrucción fue bloqueada por motivos de seguridad.'}, status=400)
            return JsonResponse({'message': response.text if hasattr(response, 'text') else 'Respuesta IA no clara.'})


        try:
            function_call_part = response.candidates[0].content.parts[0]
            function_call = getattr(function_call_part, 'function_call', None)
        except IndexError:
             print(f"DEBUG: [AI Handler] Respuesta Gemini sin 'parts'.")
             return JsonResponse({'message': response.text if hasattr(response, 'text') else 'Respuesta IA no procesable.'})

        if function_call:
            function_name = function_call.name
            args_dict = {key: value for key, value in function_call.args.items()}
            print(f"DEBUG: [AI Handler] Gemini quiere llamar a '{function_name}' con args: {args_dict}")

            # Manejo de llamadas a función específicas
            if function_name == "create_project":
                project_name = args_dict.get("name")
                description = args_dict.get("description")
                if not project_name: return JsonResponse({'error': "Nombre proyecto faltante (IA)."}, status=400)
                try:
                    project = create_project_for_user(request.user, project_name, description)
                    return JsonResponse({'message': f"Proyecto '{project.name}' creado.", 'project_id': project.id, 'type': 'project_created'})
                except ValueError as e: return JsonResponse({'error': f"Error creando proyecto: {str(e)}"}, status=400)

            elif function_name == "create_task":
                project_name = args_dict.get("project_name")
                task_desc = args_dict.get("description")
                status = args_dict.get("status", "todo")
                due_date_str = args_dict.get("due_date")
                if not project_name or not task_desc: return JsonResponse({'error': "Faltan datos tarea (IA)."}, status=400)
                try:
                    project_obj = get_project_by_user_and_name(request.user, project_name)
                    parsed_due_date = None
                    if due_date_str:
                        try: parsed_due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        except ValueError: print(f"WARN: Fecha tarea inválida '{due_date_str}'.")
                    task = create_task_for_project(project_obj, task_desc, status, parsed_due_date)
                    return JsonResponse({'message': f"Tarea '{task.description[:30]}...' añadida a '{project_obj.name}'.", 'task_id': task.id, 'type': 'task_created'})
                except Project.DoesNotExist: return JsonResponse({'error': f"Proyecto '{project_name}' no encontrado."}, status=404)
                except ValueError as e: return JsonResponse({'error': f"Error creando tarea: {str(e)}"}, status=400)

            elif function_name == "extract_expense_data":
                 description = args_dict.get("description")
                 amount = args_dict.get("amount")
                 if not description or amount is None:
                     return JsonResponse({'error': "IA no extrajo descripción o monto."}, status=400)
                 extracted_data = {
                    "description": description,
                    "amount": amount,
                    "transaction_date": args_dict.get("transaction_date"),
                    "category_name": args_dict.get("category_name_guess"),
                    "project_name": args_dict.get("project_name_guess")
                 }
                 print(f"DEBUG: [AI Handler] Datos gasto para confirmar: {extracted_data}")
                 return JsonResponse({
                    "action_needed": "confirm_expense",
                    "message": "Por favor, confirma los detalles del gasto extraídos:",
                    "extracted_data": extracted_data
                 })

            else:
                 print(f"WARN: [AI Handler] Función desconocida: {function_name}")
                 return JsonResponse({'error': f"Función IA desconocida: {function_name}"}, status=400)
        else:
            # Respuesta de texto normal de Gemini
            print(f"DEBUG: [AI Handler] Respuesta texto Gemini: '{response.text if hasattr(response, 'text') else ''}'")
            return JsonResponse({'message': response.text if hasattr(response, 'text') else 'IA no sugirió acción específica.'})

    # --- MODIFICADO: Captura específica para errores de Gemini y otros ---
    except StopCandidateException as e:
        # Error específico cuando Gemini detiene la generación (por seguridad, llamada mal formada, etc.)
        print(f"ERROR: [AI Handler] StopCandidateException: Reason={e.finish_reason}, Message={str(e)}")
        error_message = "La IA no pudo completar la solicitud."
        # Intentar obtener el finish_reason si existe
        finish_reason = getattr(e, 'finish_reason', 'UNKNOWN').upper()

        if finish_reason == "MALFORMED_FUNCTION_CALL":
            error_message = "La IA no pudo procesar la instrucción compleja. Por favor, intenta dar instrucciones más simples y separadas (una acción principal a la vez)."
        elif finish_reason == "SAFETY":
             error_message = "La instrucción fue bloqueada por motivos de seguridad."
        elif finish_reason == "RECITATION":
             error_message = "La respuesta fue bloqueada por posible recitación de contenido protegido."
        elif finish_reason == "OTHER":
             error_message = "La respuesta fue detenida por una razón no especificada por la IA."

        # Devolver un 400 Bad Request porque el problema está relacionado con la instrucción o el procesamiento de la IA
        return JsonResponse({'error': error_message}, status=400)

    except Exception as e:
        # Captura general de otros errores inesperados (conexión, código Python, etc.)
        print(f"CRITICAL ERROR en ai_command_handler: {type(e).__name__} - {str(e)}")
        print(traceback.format_exc()) # Imprime el stack trace completo del error
        # Devolver un 500 Internal Server Error
        return JsonResponse({'error': 'Ocurrió un error crítico inesperado en el servidor.'}, status=500)
    # --- FIN MODIFICADO ---