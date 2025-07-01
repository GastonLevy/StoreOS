from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms import CashMovementForm
from ..models import CashRegister, CashMovement
from checkout.models import PaymentMethod
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Crear_Movimiento_Caja')
def cash_movement_create(request):
    """
    Create a cash movement linked to the currently open cash register of the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to 'cart-create' on success, or renders form template on GET or invalid form.

    Raises:
        Http404: If no open cash register for the user and company, or if 'Efectivo' payment method doesn't exist.
    """
    # Get the open cash register associated with the user and their company
    cash_register = get_object_or_404(
        CashRegister,
        user=request.user,
        company=request.user.userprofile.company,
        status='abierta'
    )

    # Get the "Efectivo" payment method (cash)
    payment_method = get_object_or_404(PaymentMethod, name='Efectivo')

    if request.method == 'POST':
        form = CashMovementForm(request.POST)
        if form.is_valid():
            cash_movement = form.save(commit=False)
            cash_movement.cash_register = cash_register  # Link movement to current cash register
            cash_movement.payment_method = payment_method  # Set payment method to "Efectivo"
            cash_movement.company = request.user.userprofile.company  # Set company
            cash_movement.save()
            # Redirect to cart creation page after saving movement
            return redirect('cart-create')
    else:
        form = CashMovementForm()
        # Set default value for description field if none provided
        form.fields['description'].initial = ''

    return render(request, 'cash_register/cash_register_movement.html', {
        'form': form,
        'cash_register': cash_register,
    })
