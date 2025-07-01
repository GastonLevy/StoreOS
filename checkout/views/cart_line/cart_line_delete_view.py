from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from ...models import CartLine, Cart
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Eliminar_Linea_Carro')
def delete_cart_line(request, cart_id, line_id):
    """
    Deletes a line item from a cart if the cart is not completed.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_id (int): ID of the cart.
        line_id (int): ID of the cart line item to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the cart detail page on success.
        HttpResponseForbidden: If the cart is already completed and deletion is forbidden.

    Raises:
        Http404: If the cart or cart line does not exist.
    """
    # Check if the cart is marked as completed
    cart = get_object_or_404(Cart, id=cart_id)
    if cart.is_completed:
        return HttpResponseForbidden("No se puede eliminar un artículo de un carrito finalizado.")

    # If cart is not completed, proceed with deletion
    cart_line = get_object_or_404(CartLine, id=line_id, cart_id=cart_id)
    cart_line.delete()
    return HttpResponseRedirect(reverse('cart-detail', args=[cart_id]))
