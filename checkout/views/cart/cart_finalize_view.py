from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from ...models import Cart, PaymentMethod, CartLine
from accounts.models import Person, Debt
from inventory.models import Item
from cash_register.models import CashRegister
from storeos.decorators import role_required


@role_required('Admin', 'Cajero', 'Finalizar_Carro')
def finalize_cart(request, cart_id):
    """
    Finalize a cart by setting payment method, handling debts, and updating inventory.
    """
    if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
        cart = get_object_or_404(Cart, id=cart_id, company=request.user.userprofile.company)
    else:
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method')
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)

        cart.payment_method = payment_method

        if payment_method.name == 'Efectivo':
            paid_amount = Decimal(request.POST.get('paid_amount', '0'))
            total_price = cart.total_price()
            cart.payment_return = paid_amount - total_price
            cart.paid_amount = paid_amount
        else:
            cart.payment_return = None

        person_id = request.POST.get('person')
        if person_id:
            person = get_object_or_404(Person, id=person_id)
            cart.client = person

            if payment_method.name != "Cuenta Corriente":
                Debt.objects.create(
                    person=person,
                    amount=cart.total_price(),
                    cart=cart,
                    company=request.user.userprofile.company,
                    status='pagado'
                )
            else:
                Debt.objects.create(
                    person=person,
                    amount=-cart.total_price(),
                    cart=cart,
                    company=request.user.userprofile.company,
                    status='pendiente'
                )

        try:
            with transaction.atomic():
                cash_register = get_object_or_404(
                    CashRegister,
                    user=request.user,
                    company=request.user.userprofile.company,
                    status='abierta'
                )

                cash_register.carts.add(cart)

                cart_lines = CartLine.objects.filter(cart=cart)
                for line in cart_lines:
                    item = line.item

                    if item is None:
                        continue

                    if not Item.objects.filter(id=item.id).exists():
                        continue

                    item.quantity -= line.quantity
                    item.save()

                cart.is_completed = True
                cart.save()

        except Exception as e:
            print(f"Error finalizing cart: {e}")

    return redirect('cart-detail', cart_id=cart_id)