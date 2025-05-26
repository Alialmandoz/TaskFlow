# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Added for success messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import os
from datetime import datetime
import traceback
from django.utils import timezone

# Importaciones de Gemini
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException

# Modelos de Tasks
from .models import Project, Task
# Formularios de Tasks
from .forms import ProjectForm, TaskForm
# Servicios de Tasks
from .services import create_project_for_user, create_task_for_project, get_project_by_user_and_name

# Importaciones de Accounting
from accounting.models import Category # <-- Necesario para obtener las categorías del usuario
from accounting.services import create_transaction_from_data


# Vista project_list simplificada
@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user).prefetch_related('task_set').order_by('name')
    context = {'projects': projects}
    return render(request, 'tasks/project_list.html', context)

# Vistas de detalle, creación manual de proyecto y tarea
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    tasks = project.task_set.all().order_by('due_date', 'created_at')
    context = {'project': project, 'tasks': tasks}
    return render(request, 'tasks/project_detail.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('tasks:project_list')
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_form.html', {'form': form, 'page_title': 'Create Project'})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('tasks:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/project_form.html', {'form': form, 'project': project, 'page_title': 'Edit Project'})

@login_required
def task_create(request, project_pk):
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

@login_required
@require_POST
def task_delete(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    # Authorization check: Ensure the user deleting the task owns the project it belongs to
    if task.project.user != request.user:
        # Or handle as an Http404 or some other error indicating not authorized
        # For simplicity, redirecting to project list, but a specific error page might be better
        return redirect('tasks:project_list') 
    
    project_pk = task.project.pk # Save project_pk for redirection before task is deleted
    task.delete()
    # Optionally, add a Django messages framework message here
    # messages.success(request, 'Task deleted successfully.')
    return redirect('tasks:project_detail', pk=project_pk)

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
        "description": "Extrae la información detallada de un gasto o transacción financiera a partir de la instrucción del usuario. El objetivo es recopilar los detalles para una posterior confirmación antes de registrar el gasto. Se le proveerá la fecha actual como contexto.",
        "parameters": { "type": "OBJECT", "properties": { "description": { "type": "STRING", "description": "La descripción detallada del gasto (ej. 'Almuerzo con cliente X', 'Compra de licencia de software Y')." }, "amount": { "type": "NUMBER", "description": "El monto numérico del gasto (ej. 25.50, 100)." }, "transaction_date": { "type": "STRING", "description": "La fecha en que se realizó el gasto, en formato AAAA-MM-DD (ej. '2024-07-15'). Si el usuario menciona una fecha relativa (ayer, hoy, mañana), debe ser resuelta a una fecha absoluta AAAA-MM-DD basada en la fecha actual proporcionada." }, "category_name_guess": { "type": "STRING", "description": "El nombre de una categoría DE GASTOS *existente* a la que este gasto podría pertenecer (ej. 'Comida', 'Transporte', 'Software'). Si el usuario no menciona una categoría o si la categoría mencionada no parece existir, este campo puede omitirse o dejarse vacío." }, "project_name_guess": { "type": "STRING", "description": "El nombre de un proyecto *existente* al que este gasto podría estar asociado. Si el usuario no menciona un proyecto o si el gasto parece personal, omite este campo." } }, "required": ["description", "amount"] }
    }
]

# Vista del manejador de comandos IA
@login_required
@require_POST
def ai_command_handler(request):
    user_instruction_original = None
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("ERROR: GOOGLE_API_KEY no encontrada.")
            return JsonResponse({'error': 'API Key no configurada.'}, status=500)
        genai.configure(api_key=api_key)

        try:
            data = json.loads(request.body)
            action = data.get('action')
            if 'instruction' in data:
                user_instruction_original = data.get('instruction')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)

        if action == 'confirm_creation':
            confirmed_data = data.get('confirmed_data')
            if not confirmed_data:
                 return JsonResponse({'error': 'Datos de confirmación no proporcionados.'}, status=400)
            print(f"DEBUG: [AI Handler] Recibida confirmación con datos: {confirmed_data}")
            original_instruction_for_expense = confirmed_data.pop('_original_user_instruction', None)
            
            # --- MODIFICADO: Extraer los nuevos campos de categoría del frontend ---
            selected_category_id = confirmed_data.get('selected_category_id')
            create_category_name = confirmed_data.get('create_category_with_name')
            # --- FIN MODIFICADO ---

            try:
                transaction = create_transaction_from_data(
                    user=request.user,
                    description=confirmed_data.get('description'),
                    amount=confirmed_data.get('amount'),
                    transaction_date_str=confirmed_data.get('transaction_date'),
                    # --- MODIFICADO: Pasar nuevos parámetros de categoría al servicio ---
                    selected_category_id=selected_category_id,
                    create_category_with_name=create_category_name,
                    # project_name sigue igual
                    project_name=confirmed_data.get('project_name'),
                    # --- FIN MODIFICADO ---
                    original_instruction=original_instruction_for_expense
                )
                return JsonResponse({
                    'message': f"Gasto '{transaction.description[:30]}...' registrado exitosamente.",
                    'transaction_id': transaction.id,
                    'type': 'transaction_created'
                    })
            except (ValueError, TypeError) as e:
                print(f"ERROR: [AI Handler] Error al crear transacción: {str(e)}")
                return JsonResponse({'error': f"Error al registrar el gasto: {str(e)}"}, status=400)

        if not user_instruction_original:
             return JsonResponse({'error': 'Instrucción no proporcionada para procesar por IA.'}, status=400)

        current_server_date = timezone.localdate().strftime("%Y-%m-%d")
        instruction_for_gemini = f"Contexto: Hoy es {current_server_date}. Mis categorías de gastos existentes son: [{', '.join(c.name for c in Category.objects.filter(user=request.user))}]. Instrucción del usuario: {user_instruction_original}"
        
        print(f"DEBUG: [AI Handler] Enviando a Gemini (con contexto de fecha y categorías): '{instruction_for_gemini}' para {request.user.username}")

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
        response = chat.send_message(instruction_for_gemini)

        if not response.candidates or not response.candidates[0].content.parts:
            print(f"DEBUG: [AI Handler] Respuesta Gemini inesperada: {response.prompt_feedback}")
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

            if function_name == "create_project":
                # ... (sin cambios, solo pasa user_instruction_original)
                project_name = args_dict.get("name")
                description = args_dict.get("description")
                if not project_name: return JsonResponse({'error': "Nombre proyecto faltante (IA)."}, status=400)
                try:
                    project = create_project_for_user(request.user, project_name, description, original_instruction=user_instruction_original)
                    return JsonResponse({'message': f"Proyecto '{project.name}' creado.", 'project_id': project.id, 'type': 'project_created'})
                except ValueError as e: return JsonResponse({'error': f"Error creando proyecto: {str(e)}"}, status=400)


            elif function_name == "create_task":
                # ... (sin cambios, solo pasa user_instruction_original)
                project_name_for_task = args_dict.get("project_name")
                task_description = args_dict.get("description")
                status = args_dict.get("status", "todo")
                due_date_str = args_dict.get("due_date")
                if not project_name_for_task or not task_description: return JsonResponse({'error': "Faltan datos tarea (IA)."}, status=400)
                try:
                    project_obj = get_project_by_user_and_name(request.user, project_name_for_task)
                    parsed_due_date = None
                    if due_date_str:
                        try: parsed_due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        except ValueError: print(f"WARN: Fecha tarea inválida '{due_date_str}'.")
                    task = create_task_for_project(project_obj, task_description, status, parsed_due_date, original_instruction=user_instruction_original)
                    return JsonResponse({'message': f"Tarea '{task.description[:30]}...' añadida a '{project_obj.name}'.", 'task_id': task.id, 'type': 'task_created'})
                except Project.DoesNotExist: return JsonResponse({'error': f"Proyecto '{project_name_for_task}' no encontrado."}, status=404)
                except ValueError as e: return JsonResponse({'error': f"Error creando tarea: {str(e)}"}, status=400)

            elif function_name == "extract_expense_data":
                 description = args_dict.get("description")
                 amount = args_dict.get("amount")
                 if not description or amount is None:
                     return JsonResponse({'error': "IA no extrajo descripción o monto."}, status=400)
                 
                 # --- AÑADIDO: Obtener todas las categorías del usuario ---
                 user_categories_list = list(Category.objects.filter(user=request.user).values('id', 'name').order_by('name'))
                 # --- FIN AÑADIDO ---

                 extracted_data = {
                    "description": description,
                    "amount": amount,
                    "transaction_date": args_dict.get("transaction_date"),
                    "category_name_guess": args_dict.get("category_name_guess"), # La IA puede seguir adivinando
                    "project_name_guess": args_dict.get("project_name_guess"),
                    "_original_user_instruction": user_instruction_original
                 }
                 print(f"DEBUG: [AI Handler] Datos gasto para confirmar: {extracted_data}")
                 return JsonResponse({
                    "action_needed": "confirm_expense",
                    "message": "Por favor, confirma los detalles del gasto extraídos:",
                    "extracted_data": extracted_data,
                    # --- AÑADIDO: Enviar lista de categorías al frontend ---
                    "user_categories": user_categories_list
                 })
            else:
                 print(f"WARN: [AI Handler] Función desconocida: {function_name}")
                 return JsonResponse({'error': f"Función IA desconocida: {function_name}"}, status=400)
        else:
            print(f"DEBUG: [AI Handler] Respuesta texto Gemini: '{response.text if hasattr(response, 'text') else ''}'")
            return JsonResponse({'message': response.text if hasattr(response, 'text') else 'IA no sugirió acción específica.'})

    except StopCandidateException as e:
        print(f"ERROR: [AI Handler] StopCandidateException: Reason={getattr(e, 'finish_reason', 'N/A')}, Message={str(e)}")
        error_message = "La IA no pudo completar la solicitud."
        finish_reason = getattr(e, 'finish_reason', 'UNKNOWN').upper()
        if finish_reason == "MALFORMED_FUNCTION_CALL":
            error_message = "La IA no pudo procesar la instrucción compleja. Por favor, intenta dar instrucciones más simples y separadas (una acción principal a la vez)."
        elif finish_reason == "SAFETY": error_message = "La instrucción fue bloqueada por motivos de seguridad."
        elif finish_reason == "RECITATION": error_message = "Respuesta bloqueada por posible recitación de contenido."
        elif finish_reason == "OTHER": error_message = "Respuesta detenida por razón no especificada por la IA."
        return JsonResponse({'error': error_message}, status=400)
    except Exception as e:
        print(f"CRITICAL ERROR en ai_command_handler: {type(e).__name__} - {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'error': 'Ocurrió un error crítico inesperado en el servidor.'}, status=500)