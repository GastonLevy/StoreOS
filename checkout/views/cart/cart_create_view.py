from django.shortcuts import redirect, render, get_object_or_404
from ...models import Cart
from cash_register.models import CashRegister
from users.models import UserProfile
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Crear_Carro')
def cart_create(request):
    """
    Create or retrieve an active (not completed) cart for the logged-in user and their company,
    ensuring an open cash register exists for the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect or HttpResponse: 
            Redirects to the cart detail page if successful.
            Renders an error page if no open cash register is found.

    Raises:
        Http404: If the UserProfile for the user does not exist.
        PermissionDenied: If user lacks the required role (handled by decorator).
    """
    # Get user profile associated with the request user
    user_profile = get_object_or_404(UserProfile, user=request.user)
    company = user_profile.company

    # Search for an open cash register for this user and company
    cash_register = CashRegister.objects.filter(
        user=request.user,
        company=company,
        status='abierta'
    ).first()

    if not cash_register:
        # Render error page if no open cash register is found
        return render(request, 'error.html', {
            'message': 'No hay una caja abierta asociada a este usuario. Por favor, abre una caja para continuar.'
        })

    # Search for an existing non-completed cart for this user and company
    cart = Cart.objects.filter(
        user=request.user,
        company=company,
        is_completed=False,
    ).first()

    if cart:
        # Redirect to the existing cart detail
        return redirect('cart-detail', cart_id=cart.id)

    # Create a new cart if none exists
    cart = Cart.objects.create(user=request.user, company=company)
    cash_register.carts.add(cart)  # Associate the new cart with the open cash register

    # Redirect to the new cart detail
    return redirect('cart-detail', cart_id=cart.id)
