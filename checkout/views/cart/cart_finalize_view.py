from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect

from ...models import Cart, CartLine, CartPayment, PaymentMethod
from accounts.models import Person, Debt
from inventory.models import Item
from cash_register.models import CashRegister
from storeos.decorators import role_required


MONEY_QUANT = Decimal('0.01')


def money(value):
    return Decimal(str(value)).quantize(MONEY_QUANT)


def parse_money(value):
    if value in (None, ''):
        return None

    return money(value)


def build_cart_payments(request, total_price):
    payment_method_ids = request.POST.getlist('payment_method')
    amounts = request.POST.getlist('payment_amount')
    received_amounts = request.POST.getlist('received_amount')

    if payment_method_ids and not any(amounts):
        amounts = [str(total_price)]
        received_amounts = [request.POST.get('paid_amount', '')]

    payments = []

    for index, payment_method_id in enumerate(payment_method_ids):
        if not payment_method_id:
            continue

        amount = parse_money(
            amounts[index]
            if index < len(amounts)
            else None
        )

        if amount is None or amount <= 0:
            raise ValueError("Todos los pagos deben tener un importe mayor que cero.")

        payment_method = get_object_or_404(
            PaymentMethod,
            id=payment_method_id
        )

        received_amount = parse_money(
            received_amounts[index]
            if index < len(received_amounts)
            else None
        )
        change_amount = None

        if payment_method.name == 'Efectivo':
            if received_amount is None:
                received_amount = amount

            if received_amount < amount:
                raise ValueError("El efectivo recibido no puede ser menor al importe aplicado.")

            change_amount = received_amount - amount
        else:
            received_amount = None

        payments.append({
            'payment_method': payment_method,
            'amount': amount,
            'received_amount': received_amount,
            'change_amount': change_amount,
        })

    if not payments:
        raise ValueError("No se puede finalizar un carrito sin pagos válidos.")

    total_paid = sum(payment['amount'] for payment in payments)

    if total_paid != total_price:
        raise ValueError("La suma de pagos debe coincidir exactamente con el total del carrito.")

    return payments


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

    if cart.is_completed:
        messages.error(
            request,
            "No se puede finalizar un carrito ya finalizado."
        )
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

            total_price = money(cart.total_price())
            payments = build_cart_payments(request, total_price)

            first_payment = payments[0]
            cart.payment_method = (
                first_payment['payment_method']
                if len(payments) == 1
                else None
            )
            cart.finalized_total = total_price

            cash_payments = [
                payment for payment in payments
                if payment['payment_method'].name == 'Efectivo'
            ]
            if len(cash_payments) == 1:
                cart.paid_amount = cash_payments[0]['received_amount']
                cart.payment_return = cash_payments[0]['change_amount']
            else:
                cart.paid_amount = None
                cart.payment_return = None

            person_id = request.POST.get('person')
            person = None

            if person_id:
                person = get_object_or_404(
                    Person,
                    id=person_id
                )

                cart.client = person

            cart.payments.all().delete()

            for payment in payments:
                CartPayment.objects.create(
                    cart=cart,
                    payment_method=payment['payment_method'],
                    amount=payment['amount'],
                    received_amount=payment['received_amount'],
                    change_amount=payment['change_amount'],
                )

                if not person:
                    continue

                if payment['payment_method'].name != "Cuenta Corriente":
                    Debt.objects.create(
                        person=person,
                        amount=payment['amount'],
                        cart=cart,
                        company=company,
                        status='pagado'
                    )
                else:
                    Debt.objects.create(
                        person=person,
                        amount=-payment['amount'],
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
