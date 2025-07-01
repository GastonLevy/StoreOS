from django.contrib import admin
from .models import Cart, CartLine, PaymentMethod

# Administrador para Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company', 'payment_method', 'payment_return', 'is_completed', 'created_at', 'updated_at')  # Muestra los campos relevantes
    search_fields = ('user__username', 'company__name', 'payment_method__name')  # Permite buscar por usuario, empresa o método de pago
    list_filter = ('is_completed', 'company', 'payment_method')  # Permite filtrar por estado de completado, empresa y método de pago
    ordering = ('-created_at',)  # Ordena por fecha de creación descendente


# Administrador para CartLine
@admin.register(CartLine)
class CartLineAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'quantity', 'price', 'name', 'total')  # Asegúrate de agregar 'total'
    search_fields = ('cart__user__username', 'item__name')  # Permite buscar por usuario del carrito y nombre del item
    list_filter = ('cart', 'item')  # Permite filtrar por carrito e item
    ordering = ('cart',)  # Ordena por carrito por defecto



# Administrador para PaymentMethod
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')  # Muestra 'name' y 'is_active'
    search_fields = ('name',)  # Permite buscar por 'name'
    list_filter = ('is_active',)  # Permite filtrar por si está activo
    ordering = ('name',)  # Ordena por 'name' por defecto
