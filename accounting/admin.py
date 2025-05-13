# D:\trabajo\Propio\IA\programing\TaskFlow\accounting\admin.py

from django.contrib import admin
from .models import Category, Transaction
from tasks.models import Project # Para filtrar en formfield_for_foreignkey

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if not request.user.is_superuser and not hasattr(obj, 'user'):
                obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'transaction_date', 'category', 'project', 'user', 'type', 'original_instruction') # <-- AÑADIDO a list_display
    list_filter = ('transaction_date', 'user', 'category', 'project', 'type')
    search_fields = ('description', 'notes', 'user__username', 'project__name', 'category__name', 'original_instruction') # <-- AÑADIDO a search_fields
    list_editable = ('amount', 'category')
    date_hierarchy = 'transaction_date'
    fieldsets = (
        (None, {
            'fields': ('user', 'description', 'amount', 'type', 'transaction_date')
        }),
        ('Asociaciones', {
            'fields': ('category', 'project')
        }),
        ('Notas Adicionales', {
            # --- MODIFICADO: Añadir original_instruction aquí ---
            'fields': ('notes', 'original_instruction'),
            'classes': ('collapse',)
        }),
    )
    # --- AÑADIDO: Hacer original_instruction readonly en el admin si se desea ---
    readonly_fields = ('original_instruction',)


    def save_model(self, request, obj, form, change):
        if not obj.pk:
             if not request.user.is_superuser and not hasattr(obj, 'user'): # Si no es superuser y el usuario no está seteado
                obj.user = request.user # Asignar el usuario actual
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "category":
                kwargs["queryset"] = Category.objects.filter(user=request.user)
            if db_field.name == "project":
                kwargs["queryset"] = Project.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)