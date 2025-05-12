# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\forms.py

from django import forms
from .models import Transaction, Category # Importamos nuestros modelos de accounting
from tasks.models import Project # Importamos el modelo Project de la app tasks

class TransactionForm(forms.ModelForm):
    """
    Formulario para crear y actualizar Transacciones (gastos).
    """
    # Personalización de campos si es necesario, por ejemplo, para el widget de fecha
    transaction_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), # Usa el input de tipo fecha del navegador
        label="Fecha de la Transacción"
    )

    # Queryset para el campo 'category' y 'project' se ajustará en la vista
    # para mostrar solo las opciones relevantes al usuario.
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(), # Queryset vacío inicialmente, se llenará en la vista
        required=False, # Permitir no categorizar inicialmente
        label="Categoría"
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.none(), # Queryset vacío inicialmente, se llenará en la vista
        required=False, # Un gasto puede no estar asociado a un proyecto
        label="Proyecto Asociado (Opcional)"
    )

    class Meta:
        model = Transaction
        # Campos que queremos en el formulario
        fields = [
            'description', 
            'amount', 
            'transaction_date', 
            'type', # Aunque sea solo 'expense' por ahora, es bueno tenerlo si se expande
            'category', 
            'project', 
            'notes'
        ]
        # Excluimos 'user' porque se asignará automáticamente en la vista.
        # Excluimos 'created_at' y 'updated_at' porque son automáticos.

        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}), # Hacer el campo de notas un poco más grande
            'description': forms.TextInput(attrs={'placeholder': 'Ej: Almuerzo con cliente, Compra de software'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Ej: 25.50'}),
        }
        labels = {
            'description': 'Descripción del Gasto',
            'amount': 'Monto ($)', # Puedes ajustar la moneda o hacerlo dinámico
            'type': 'Tipo de Transacción',
            'notes': 'Notas Adicionales',
        }
        help_texts = {
            'type': 'Actualmente solo se registran gastos.',
        }

    def __init__(self, *args, **kwargs):
        # Es crucial obtener el 'user' aquí para filtrar los querysets de category y project.
        # La vista pasará el usuario al instanciar el formulario.
        user = kwargs.pop('user', None) # Extraemos el usuario de los kwargs
        super().__init__(*args, **kwargs)

        if user:
            # Filtramos el queryset del campo 'category' para mostrar solo las del usuario actual.
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')
            # Filtramos el queryset del campo 'project' para mostrar solo los del usuario actual.
            self.fields['project'].queryset = Project.objects.filter(user=user).order_by('name')
        else:
            # Si no hay usuario (ej. en algún caso raro o si se usa sin contexto de usuario),
            # dejamos los querysets vacíos o podríamos mostrar todos si es un superadmin,
            # pero para la creación por usuario, el filtro es esencial.
            self.fields['category'].queryset = Category.objects.none()
            self.fields['project'].queryset = Project.objects.none()

        # Si el tipo de transacción es fijo a 'expense' y no quieres que el usuario lo vea/modifique
        # podrías ocultarlo o deshabilitarlo, pero al ser un ModelForm basado en `fields`,
        # se incluirá. Si solo quieres gastos, podrías quitar 'type' de `fields`
        # y asignarlo directamente en la vista antes de guardar.
        # Por ahora lo dejamos visible pero con default 'expense'.
        # self.fields['type'].disabled = True # Ejemplo si quisieras deshabilitarlo
        self.fields['type'].initial = 'expense'