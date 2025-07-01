from django.contrib import admin
from .models import CashRegister, CashMovement

# Administrador para CashRegister
@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'status', 'opening_balance', 'closing_balance', 'created_at', 'closed_at')  # Campos relevantes en la lista
    search_fields = ('user__username', 'company__name')  # Permite buscar por usuario y nombre de la empresa
    list_filter = ('status', 'company')  # Filtra por estado y empresa
    list_editable = ('status', 'closing_balance')  # Permite editar el estado y el saldo final desde la lista
    ordering = ('-created_at',)  # Ordena por fecha de apertura descendente
    readonly_fields = ('created_at', 'closed_at')  # Los campos de fecha de apertura y cierre son solo lectura

    def total_balance(self, obj):
        # Agrega un campo extra en la lista que muestre el saldo total calculado
        return obj.calculate_total()
    total_balance.short_description = 'Saldo Total'  # Etiqueta para la columna
    list_display += ('total_balance',)  # Añadido a la lista de campos a mostrar


# Administrador para CashMovement
@admin.register(CashMovement)
class CashMovementAdmin(admin.ModelAdmin):
    list_display = ('cash_register', 'payment_method', 'type', 'amount', 'created_at', 'cart')  # Muestra los campos relevantes
    search_fields = ('cash_register__user__username', 'payment_method__name', 'cart__id')  # Permite buscar por usuario de caja, método de pago y carrito
    list_filter = ('type', 'payment_method', 'cash_register')  # Filtra por tipo, método de pago y caja
    ordering = ('-created_at',)  # Ordena por fecha de creación descendente
    readonly_fields = ('created_at',)  # Solo lectura para el campo de fecha

