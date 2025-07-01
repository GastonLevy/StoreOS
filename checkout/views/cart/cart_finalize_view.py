from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from ...models import Cart, PaymentMethod, CartLine
from accounts.models import Person, Debt
from inventory.models import Item  # Make sure to import the Item model
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Finalizar_Carro')
def finalize_cart(request, cart_id):
    """
    Finalize a cart by setting payment method, handling debts, and updating inventory.

    Args:
        request (HttpRequest): The HTTP request object, expects POST with:
            - payment_method (str): ID of the payment method.
            - paid_amount (str, optional): Amount paid by the client (used if payment is cash).
            - person (str, optional): ID of the client (Person) associated with the cart.
        cart_id (int): ID of the cart to finalize.

    Returns:
        HttpResponseRedirect: Redirects to the cart detail page.

    Raises:
        Http404: If Cart, PaymentMethod, or Person do not exist or user lacks permission.
        Exception: Propagates any exception raised during the transaction block.
    """
    # Check if user has access to the cart based on permissions
    if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
        cart = get_object_or_404(Cart, id=cart_id, company=request.user.userprofile.company)
    else:
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == 'POST':
        # Get payment method by ID from POST data
        payment_method_id = request.POST.get('payment_method')
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)

        # Assign payment method to the cart
        cart.payment_method = payment_method

        if payment_method.name == 'Efectivo':
            # Calculate change if payment is cash
            paid_amount = Decimal(request.POST.get('paid_amount', '0'))
            total_price = cart.total_price()
            cart.payment_return = paid_amount - total_price
            cart.paid_amount = paid_amount
        else:
            cart.payment_return = None

        # Assign client (Person) if provided
        person_id = request.POST.get('person')
        if person_id:
            person = get_object_or_404(Person, id=person_id)
            cart.client = person

            # Create Debt depending on payment method
            if payment_method.name != "Cuenta Corriente":
                # For non "Cuenta Corriente", create a paid debt
                Debt.objects.create(
                    person=person,
                    amount=cart.total_price(),
                    cart=cart,
                    company=request.user.userprofile.company,
                    status='pagado'
                )
            else:
                # For "Cuenta Corriente", create a pending debt with negative amount
                Debt.objects.create(
                    person=person,
                    amount=-cart.total_price(),
                    cart=cart,
                    company=request.user.userprofile.company,
                    status='pendiente'
                )

        try:
            with transaction.atomic():
                # Decrement inventory quantities for each cart line
                cart_lines = CartLine.objects.filter(cart=cart)
                for line in cart_lines:
                    item = line.item

                    if item is None:
                        continue  # Skip if no associated item

                    # Skip if item no longer exists in inventory (deleted or temporary)
                    if not Item.objects.filter(id=item.id).exists():
                        continue

                    item.quantity -= line.quantity
                    item.save()

                # Mark cart as completed and save
                cart.is_completed = True
                cart.save()

        except Exception as e:
            # Log the error, you can extend this to handle errors better
            print(f"Error finalizing cart: {e}")
            # You might want to redirect to an error page or notify the user here

    return redirect('cart-detail', cart_id=cart_id)
