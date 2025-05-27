# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\models.py

from django.db import models
from django.contrib.auth.models import User
from tasks.models import Project # Para asociar a un proyecto de la app 'tasks'
from django.utils import timezone

class Category(models.Model):
    """
    Representa una categoría para las transacciones (gastos/ingresos).
    """
    name = models.CharField(max_length=100) # unique=True se maneja con unique_together
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario al que pertenece esta categoría")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        unique_together = ('name', 'user') # Nombre de categoría único por usuario

    def __str__(self):
        return f"{self.name} (Usuario: {self.user.username})"

class Transaction(models.Model):
    """
    Representa una transacción financiera, principalmente un gasto.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('expense', 'Gasto'),
        # ('income', 'Ingreso'),
    ]

    description = models.CharField(max_length=255, help_text="Descripción del gasto.")
    currency = models.CharField(
        max_length=3,
        choices=[("ARS", "Argentine Peso"), ("USD", "US Dollar")],
        default="ARS",
        help_text="Currency of the transaction."
    )
    original_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,  # Temporarily allow null
        blank=True, # Temporarily allow blank
        help_text="Amount in the original currency (e.g., ARS or USD)."
    )
    exchange_rate_usd = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Exchange rate (ARS per 1 USD) if the original transaction was in USD."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount converted to ARS. If original was USD, this is original_amount * exchange_rate_usd."
    )
    transaction_date = models.DateField(default=timezone.now, help_text="Fecha en que se realizó el gasto.")
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        default='expense',
        help_text="Tipo de transacción (actualmente solo Gasto)."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Categoría del gasto."
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Proyecto de TaskFlow al que está asociado este gasto (opcional)."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Usuario que registró el gasto."
    )
    notes = models.TextField(blank=True, null=True, help_text="Notas adicionales sobre el gasto (opcional).")
    # --- AÑADIDO ---
    original_instruction = models.TextField(
        null=True,
        blank=True,
        help_text="La instrucción original del usuario si fue creado vía IA."
    )
    # --- FIN AÑADIDO ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-transaction_date', '-created_at']

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.user.username})"