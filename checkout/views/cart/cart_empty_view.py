from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from ...models import Cart
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Vaciar_Carro')
def empty_cart(request, cart_id):
    """
    Empty all lines in a cart if it is not completed.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_id (int): ID of the cart to empty.

    Returns:
        HttpResponseRedirect: Redirects to the cart detail page.

    Raises:
        Http404: If Cart with the given ID does not exist.
    """
    cart = get_object_or_404(Cart, id=cart_id)

    # Check if the cart is completed
    if cart.is_completed:
        messages.error(request, "No se puede vaciar un carrito finalizado.")
        return redirect('cart-detail', cart_id=cart.id)

    # Empty the cart lines if cart is not completed
    cart.cart_lines.all().delete()
    messages.success(request, "Carrito vaciado correctamente.")
    return redirect('cart-detail', cart_id=cart.id)
