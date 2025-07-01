from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from ...models import Cart
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Eliminar_Carro')
def delete_cart(request, cart_id):
    """
    Delete a cart if it is not completed.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_id (int): The ID of the cart to delete.

    Returns:
        HttpResponseRedirect: Redirects to the cart list page.

    Raises:
        Http404: If the cart does not exist.
        PermissionDenied: If user lacks the required role (handled by decorator).
    """
    # Check if the cart is completed
    cart = get_object_or_404(Cart, id=cart_id)
    if cart.is_completed:
        messages.error(request, "No se puede eliminar un carrito finalizado.")
        return redirect('cart-list')  # Redirect to cart list

    # Delete the cart if not completed
    cart.delete()
    messages.success(request, "Carrito eliminado correctamente.")
    return redirect('cart-list')  # Redirect to cart list
