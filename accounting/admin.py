# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\admin.py

from django.contrib import admin
from .models import Category, Transaction # Importamos nuestros modelos

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuración de la administración para el modelo Category.
    """
    list_display = ('name', 'user') # Campos a mostrar en la lista de categorías
    list_filter = ('user',) # Permite filtrar por usuario
    search_fields = ('name', 'user__username') # Permite buscar por nombre de categoría o nombre de usuario
    # Asegura que al crear una categoría desde el admin, el usuario actual se asigne si no es superuser.
    # O mejor aún, que solo el usuario pueda ver/editar sus propias categorías.
    # Esto requiere un poco más de lógica en get_queryset y save_model si queremos una restricción estricta.
    # Por ahora, un superusuario verá todas. Un usuario normal no debería tener acceso al admin
    # a menos que le demos permisos específicos.

    # Para simplificar la creación para el usuario actual, si no es superuser:
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Si es un objeto nuevo
            if not request.user.is_superuser and not hasattr(obj, 'user'): # Si no es superuser y el usuario no está seteado
                obj.user = request.user # Asignar el usuario actual
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs # El superusuario ve todas las categorías
        return qs.filter(user=request.user) # Otros usuarios solo ven sus propias categorías

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Configuración de la administración para el modelo Transaction.
    """
    list_display = ('description', 'amount', 'transaction_date', 'category', 'project', 'user', 'type')
    list_filter = ('transaction_date', 'user', 'category', 'project', 'type')
    search_fields = ('description', 'notes', 'user__username', 'project__name', 'category__name')
    list_editable = ('amount', 'category') # Campos que se pueden editar directamente en la lista (cuidado con esto)
    date_hierarchy = 'transaction_date' # Añade navegación por fechas
    fieldsets = (
        (None, {
            'fields': ('user', 'description', 'amount', 'type', 'transaction_date')
        }),
        ('Asociaciones', {
            'fields': ('category', 'project')
        }),
        ('Notas Adicionales', {
            'fields': ('notes',),
            'classes': ('collapse',) # Hace esta sección colapsable
        }),
    )

    # Similar a CategoryAdmin, para asignar el usuario automáticamente y filtrar por usuario
    def save_model(self, request, obj, form, change):
        if not obj.pk:
             if not request.user.is_superuser and not hasattr(obj, 'user'):
                obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user) # Usuarios solo ven sus transacciones
        
    # Para asegurar que los ForeignKeys a Category y Project solo muestren
    # las opciones pertenecientes al usuario actual (si no es superuser)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "category":
                kwargs["queryset"] = Category.objects.filter(user=request.user)
            if db_field.name == "project":
                # Asumiendo que el modelo Project también tiene un campo 'user'
                from tasks.models import Project # Importación local
                kwargs["queryset"] = Project.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Otra forma más simple de registrar si no necesitas personalización:
# admin.site.register(Category)
# admin.site.register(Transaction)