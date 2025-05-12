# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\models.py

from django.db import models
from django.contrib.auth.models import User # Para asociar a un usuario
from tasks.models import Project # Para asociar a un proyecto de la app 'tasks'
from django.utils import timezone # Para la fecha por defecto

class Category(models.Model):
    """
    Representa una categoría para las transacciones (gastos/ingresos).
    Ejemplos: "Alimentación", "Transporte", "Materiales de Proyecto", "Software".
    """
    name = models.CharField(max_length=100, unique=True) # Nombre único para la categoría
    # El tipo podría ser útil si en el futuro quieres diferenciar categorías de Ingreso vs Egreso.
    # TYPE_CHOICES = [('expense', 'Gasto'), ('income', 'Ingreso')]
    # type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario al que pertenece esta categoría")
    # Opcional: para jerarquía de categorías
    # parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        # Asegura que el nombre de la categoría sea único por usuario para evitar duplicados personales
        unique_together = ('name', 'user')


    def __str__(self):
        return f"{self.name} (Usuario: {self.user.username})"

class Transaction(models.Model):
    """
    Representa una transacción financiera, principalmente un gasto.
    Puede estar asociada a un proyecto específico o ser un gasto general/personal.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('expense', 'Gasto'),
        # ('income', 'Ingreso'), # Podríamos añadir ingresos más adelante
    ]

    description = models.CharField(max_length=255, help_text="Descripción del gasto.")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto del gasto.")
    transaction_date = models.DateField(default=timezone.now, help_text="Fecha en que se realizó el gasto.")
    
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        default='expense',
        help_text="Tipo de transacción (actualmente solo Gasto)."
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, # Si se borra la categoría, no borrar la transacción, solo desasociar
        null=True, 
        blank=True, # Permitir transacciones sin categorizar inicialmente
        help_text="Categoría del gasto."
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.SET_NULL, # Si se borra el proyecto, no borrar la transacción
        null=True, 
        blank=True, # El gasto puede no estar asociado a un proyecto (gasto personal)
        help_text="Proyecto de TaskFlow al que está asociado este gasto (opcional)."
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, # Si se borra el usuario, se borran sus transacciones
        help_text="Usuario que registró el gasto."
    )
    notes = models.TextField(blank=True, null=True, help_text="Notas adicionales sobre el gasto (opcional).")
    created_at = models.DateTimeField(auto_now_add=True) # Fecha de creación del registro
    updated_at = models.DateTimeField(auto_now=True)   # Fecha de última actualización

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-transaction_date', '-created_at'] # Ordenar por fecha de transacción y luego por creación

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.user.username})"