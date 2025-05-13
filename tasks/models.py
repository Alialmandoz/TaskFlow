# D:\trabajo\Propio\IA\programing\TaskFlow\tasks\models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Necesario si usamos completed_at con auto_now

# Entidad Proyecto: El contenedor principal.
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # --- AÑADIDO ---
    original_instruction = models.TextField(
        null=True,
        blank=True,
        help_text="La instrucción original del usuario si fue creado vía IA."
    )
    # --- FIN AÑADIDO ---

    def __str__(self):
        return f"{self.name} (by {self.user.username})"

# Entidad Tarea: Lo que queremos gestionar, contenido dentro de un proyecto.
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Por hacer'),
        ('doing', 'En progreso'),
        ('done', 'Completada'),
    ]

    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    # --- AÑADIDO ---
    original_instruction = models.TextField(
        null=True,
        blank=True,
        help_text="La instrucción original del usuario si fue creado vía IA."
    )
    # --- FIN AÑADIDO ---

    def __str__(self):
        return f"{self.description[:50]}... (Status: {self.status})"

    def mark_as_completed(self):
        if self.status != 'done':
            self.status = 'done'
            # Usar timezone.now() para la consistencia con auto_now_add
            self.completed_at = timezone.now()
            self.save()

    def mark_as_todo(self): # Ejemplo de otra acción
        if self.status == 'done':
            self.status = 'todo'
            self.completed_at = None
            self.save()