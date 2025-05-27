# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\forms.py

from django import forms
from .models import Transaction, Category # Importamos Category para el filtro
from tasks.models import Project

class TransactionForm(forms.ModelForm):
    """
    Formulario para crear y actualizar Transacciones (gastos).
    (Sin cambios respecto a la versión anterior)
    """
    transaction_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label="Fecha de la Transacción"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        label="Categoría"
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.none(),
        required=False,
        label="Proyecto Asociado (Opcional)"
    )

    class Meta:
        model = Transaction
        fields = [
            'description',
            'original_amount', # User inputs amount in original currency
            'currency',        # User selects currency
            'transaction_date',
            'type',
            'category',
            'project',
            'notes'
            # 'amount' is removed from here, will be calculated
            # 'exchange_rate_usd' is also removed, will be set in the view
            # 'original_instruction' no se incluye aquí, se maneja programáticamente
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'description': forms.TextInput(attrs={'placeholder': 'Ej: Almuerzo con cliente'}),
            'original_amount': forms.NumberInput(attrs={'placeholder': 'Ej: 25.50'}),
            # transaction_date widget is defined at field level
        }
        labels = {
            'description': 'Descripción del Gasto',
            'original_amount': 'Monto (Original)', # Will be changed in __init__
            'currency': 'Moneda',
            'type': 'Tipo de Transacción',
            'notes': 'Notas Adicionales',
        }
        help_texts = {
            'type': 'Actualmente solo se registran gastos.',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['original_amount'].label = "Amount" # As per instruction
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')
            self.fields['project'].queryset = Project.objects.filter(user=user).order_by('name')
        else:
            self.fields['category'].queryset = Category.objects.none()
            self.fields['project'].queryset = Project.objects.none()
        self.fields['type'].initial = 'expense'

# --- AÑADIDO: Formulario para filtrar transacciones ---
class TransactionFilterForm(forms.Form):
    """
    Formulario para filtrar la lista de transacciones.
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(), # Se llenará dinámicamente en la vista
        required=False, # Permitir no filtrar por categoría (mostrar todas)
        label="Filtrar por Categoría",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}) # Estilo Bootstrap
    )
    # Podríamos añadir más filtros aquí en el futuro (ej. rango de fechas, proyecto)
    # start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}))
    # end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}))

    def __init__(self, *args, **kwargs):
        # El usuario es necesario para poblar el queryset de categorías
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')
        else:
            # Si no hay usuario (ej. admin global), podríamos mostrar todas o ninguna
            # Para un usuario normal, esto no debería pasar si la vista está protegida.
            self.fields['category'].queryset = Category.objects.none()
# --- FIN AÑADIDO ---