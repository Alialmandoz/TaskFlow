from django.db import models
from django.contrib.auth.models import User # Importamos el modelo de usuario de Django

# Entidad Proyecto: El contenedor principal.
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # Relación: Un proyecto pertenece a UN usuario. Esta es una clave foránea.
    # on_delete=models.CASCADE: Si el usuario se elimina, también se eliminan sus proyectos.
    # Desde una perspectiva sistémica, define una fuerte dependencia existencial del Project con el User.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # Captura la dinámica de creación

    # Método para representación legible del objeto (útil en la administración de Django)
    def __str__(self):
        return f"{self.name} (by {self.user.username})"

# Entidad Tarea: Lo que queremos gestionar, contenido dentro de un proyecto.
class Task(models.Model):
    # Opciones de estado: Definimos los estados posibles (parte de la dinámica del ciclo de vida de la tarea)
    STATUS_CHOICES = [
        ('todo', 'Por hacer'),
        ('doing', 'En progreso'),
        ('done', 'Completada'),
    ]

    description = models.TextField()
    # Campo de estado con opciones predefinidas. Define el comportamiento de estado de la tarea.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    # Relación: Una tarea pertenece a UN proyecto. ¡Esta es la clave estructural de Opción 1!
    # on_delete=models.CASCADE: Si el proyecto se elimina, todas sus tareas también se eliminan.
    # Define la dependencia existencial de Task con Project.
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Fecha de vencimiento: introduce la dimensión temporal y la dinámica de urgencia.
    due_date = models.DateField(null=True, blank=True)
    # Fecha de completado: registra un evento clave en la dinámica de la tarea.
    completed_at = models.DateTimeField(null=True, blank=True)

    # Método para representación legible del objeto
    def __str__(self):
        return f"{self.description[:50]}... (Status: {self.status})"

    # Opcional: Un método simple para cambiar el estado de forma controlada.
    # Encapsula parte de la lógica de negocio ("comportamiento").
    def mark_as_completed(self):
        if self.status != 'done':
            self.status = 'done'
            # Usa auto_now=True para actualizar la fecha y hora al guardar
            self.completed_at = models.DateTimeField(auto_now=True)
            self.save()