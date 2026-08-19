from decimal import Decimal

from django.contrib import messages
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
    Finalize a cart only if the user has an open cash register.
    If the cart belongs to another cash register, associate it
    with the currently open cash register.
    """

    company = request.user.userprofile.company

    if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
        cart = get_object_or_404(
            Cart,
            id=cart_id,
            company=company
        )
    else:
        cart = get_object_or_404(
            Cart,
            id=cart_id,
            user=request.user,
            company=company
        )

    if request.method != 'POST':
        return redirect('cart-detail', cart_id=cart_id)

    # La caja abierta es obligatoria para finalizar
    cash_register = CashRegister.objects.filter(
        user=request.user,
        company=company,
        status='abierta'
    ).first()

    if not cash_register:
        messages.error(
            request,
            "No puedes finalizar el carrito porque no tienes una caja abierta."
        )
        return redirect('cart-detail', cart_id=cart_id)

    payment_method_id = request.POST.get('payment_method')
    payment_method = get_object_or_404(
        PaymentMethod,
        id=payment_method_id
    )

    try:
        with transaction.atomic():

            # Si el carrito estaba asociado a otra caja,
            # quitar esa asociación y usar la caja actualmente abierta.
            previous_cash_registers = cart.cash_registers.exclude(
                pk=cash_register.pk
            )

            for previous_cash_register in previous_cash_registers:
                previous_cash_register.carts.remove(cart)

            if not cash_register.carts.filter(pk=cart.pk).exists():
                cash_register.carts.add(cart)

            cart.payment_method = payment_method
            total_price = cart.total_price()
            cart.finalized_total = total_price

            if payment_method.name == 'Efectivo':
                paid_amount = Decimal(
                    request.POST.get('paid_amount', '0')
                )

                cart.payment_return = paid_amount - total_price
                cart.paid_amount = paid_amount
            else:
                cart.payment_return = None
                cart.paid_amount = None

            person_id = request.POST.get('person')

            if person_id:
                person = get_object_or_404(
                    Person,
                    id=person_id
                )

                cart.client = person

                if payment_method.name != "Cuenta Corriente":
                    Debt.objects.create(
                        person=person,
                        amount=total_price,
                        cart=cart,
                        company=company,
                        status='pagado'
                    )
                else:
                    Debt.objects.create(
                        person=person,
                        amount=-total_price,
                        cart=cart,
                        company=company,
                        status='pendiente'
                    )

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
        messages.error(
            request,
            f"No se pudo finalizar el carrito: {e}"
        )
        return redirect('cart-detail', cart_id=cart_id)

    messages.success(request, "Venta finalizada correctamente.")

    return redirect('cart-detail', cart_id=cart_id)
