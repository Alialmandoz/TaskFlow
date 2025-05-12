# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\admin.py

from django.contrib import admin
from .models import Project, Task # Importamos nuestros modelos

# Registramos el modelo Project en el sitio de administración.
admin.site.register(Project)

# Registramos el modelo Task en el sitio de administración.
admin.site.register(Task)

# Opcional pero recomendado para mejor visualización:
# Podemos crear clases ModelAdmin para personalizar la apariencia en el admin.
# Esto refina la interfaz de control del sistema.

# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('name', 'user', 'created_at') # Campos a mostrar en la lista
#     search_fields = ('name', 'description') # Campos por los que se puede buscar

# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('description', 'project', 'status', 'due_date', 'completed_at')
#     list_filter = ('status', 'project', 'due_date') # Filtros en la barra lateral
#     search_fields = ('description',)

# # Re-registramos usando las clases ModelAdmin personalizadas si las defines
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Task, TaskAdmin)