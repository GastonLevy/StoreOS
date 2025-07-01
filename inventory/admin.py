from django.contrib import admin
from .models import Category, Item

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')  # Muestra 'name' y 'company' en la lista
    search_fields = ('name',)  # Permite buscar por 'name'
    list_filter = ('company',)  # Permite filtrar por 'company'
    ordering = ('name',)  # Ordenar por 'name' por defecto


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'price', 'quantity', 'stockable', 'company')  # Muestra los campos de interés
    search_fields = ('name', 'barcode')  # Permite buscar por 'name' y 'barcode'
    list_filter = ('company', 'categories', 'stockable')  # Permite filtrar por 'company', 'categories', y 'stockable'
    list_editable = ('price', 'quantity', 'stockable')  # Permite editar directamente en la lista
    raw_id_fields = ('categories',)  # Utiliza el campo de búsqueda por ID para 'categories' si la lista es muy larga
    ordering = ('name',)  # Ordena por 'name' por defecto
