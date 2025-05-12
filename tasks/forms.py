# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\forms.py

from django import forms
# Importamos ambos modelos ahora, ya que ambos tendrán formularios asociados
from .models import Project, Task # <-- Asegúrate de importar Task

class ProjectForm(forms.ModelForm):
    """
    Formulario basado en el modelo Project para crear o actualizar proyectos.
    """
    class Meta:
        model = Project
        # Incluimos solo los campos que el usuario puede editar directamente
        fields = ['name', 'description']
        # Excluimos 'user' porque lo asignaremos automáticamente en la vista
        # Excluimos 'created_at' porque auto_now_add lo maneja
        # exclude = ['user', 'created_at'] # Esta sería otra forma de hacerlo
        
# NUEVO: Formulario para el modelo Task
class TaskForm(forms.ModelForm):
    """
    Formulario basado en el modelo Task para crear o actualizar tareas.
    """
    class Meta:
        model = Task
        # Listamos los campos del modelo Task que queremos incluir en el formulario.
        # 'description' y 'due_date' son los campos que el usuario introducirá.
        # Incluiremos 'status' para permitir al usuario establecer el estado inicial
        fields = ['description', 'status', 'due_date']
        # Excluimos 'project' porque lo asignaremos en la vista basándonos en la URL.
        # Excluimos 'created_at' y 'completed_at' porque se manejan automáticamente o en la lógica de la vista.
        # exclude = ['project', 'created_at', 'completed_at'] # Otra forma con exclude