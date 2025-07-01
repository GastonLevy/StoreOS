# urls.py
from django.urls import path
from .views import (
    cart_create,
    cart_detail,
    cart_list,
    delete_cart,
    empty_cart,
    finalize_cart,

    delete_cart_line
)

urlpatterns = [
    path('cart/create/', cart_create, name='cart-create'),  # Crear un nuevo carrito
    path('cart/<int:cart_id>/', cart_detail, name='cart-detail'),  # Ver detalle de un carrito
    path('cart/<int:cart_id>/delete/', delete_cart, name='cart-delete'),  # Eliminar un carrito específico
    path('cart/<int:cart_id>/empty/', empty_cart, name='cart-empty'),  # Vaciar un carrito de sus líneas
    path('cart/<int:cart_id>/finalize/', finalize_cart, name='cart-finalize'),  # Finalizar un carrito
    path('carts/', cart_list, name='cart-list'),  # Listar todos los carritos del usuario

    path('cart/<int:cart_id>/delete-line/<int:line_id>/', delete_cart_line, name='delete-cart-line'),
]
