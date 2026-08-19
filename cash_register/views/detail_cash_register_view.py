from decimal import Decimal

from django.contrib.auth.models import Group
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render

from checkout.models import CartLine
from storeos.decorators import role_required
from ..models.cash_register_model import CashRegister


@role_required('Admin', 'Cajero', 'Detalle_Caja')
def cash_register_detail_view(request, pk):
    """
    Display detailed information of a specific cash register including sales,
    cash income, expenses, balance, and payment method summaries.
    """

    is_admin_or_superadmin = (
        request.user.is_superuser
        or Group.objects.filter(
            name='Admin',
            user=request.user
        ).exists()
    )

    if is_admin_or_superadmin:
        cash_register = get_object_or_404(
            CashRegister,
            pk=pk,
            company=request.user.userprofile.company
        )
    else:
        cash_register = get_object_or_404(
            CashRegister,
            pk=pk,
            user=request.user
        )

    completed_carts = cash_register.carts.filter(
        is_completed=True
    ).distinct()

    # Total sales from all completed carts
    ingresos = sum(
        cart.total_price()
        for cart in completed_carts
    )

    # Real sales paid in cash.
    # This is the sale amount, NOT the amount handed over by the customer.
    efectivo_ingresos = sum(
        cart.total_price()
        for cart in completed_carts.filter(
            payment_method__name='Efectivo'
        )
    )

    # Cash register movements
    total_ingresos = sum(
        movement.amount
        for movement in cash_register.movements.filter(
            type='ingreso'
        )
    )

    total_egresos = sum(
        movement.amount
        for movement in cash_register.movements.filter(
            type='egreso'
        )
    )

    # Net result of manual cash movements
    movimientos = total_ingresos - total_egresos

    # Expected physical cash balance
    balance_total = (
        cash_register.opening_balance
        + efectivo_ingresos
        + total_ingresos
        - total_egresos
    )

    # Income grouped by payment method
    payment_method_totals_by_name = {}

    for cart in completed_carts.select_related('payment_method'):
        payment_method_name = (
            cart.payment_method.name
            if cart.payment_method
            else 'Sin método de pago'
        )

        payment_method_totals_by_name.setdefault(
            payment_method_name,
            Decimal('0.00')
        )
        payment_method_totals_by_name[payment_method_name] += cart.sale_total()

    payment_method_totals = [
        {
            'payment_method__name': payment_method_name,
            'total': total,
        }
        for payment_method_name, total in payment_method_totals_by_name.items()
    ]
    payment_method_totals.sort(
        key=lambda payment: payment['total'],
        reverse=True
    )

    # Total quantity moved per item in completed carts
    item_movement = (
        CartLine.objects
        .filter(cart__in=completed_carts)
        .values('name')
        .annotate(total_quantity=Sum('quantity'))
    )

    context = {
        'cash_register': cash_register,
        'ingresos': ingresos,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'movimientos': movimientos,
        'balance_total': balance_total,
        'payment_method_totals': payment_method_totals,
        'efectivo_ingresos': efectivo_ingresos,
        'lista_movimientos': item_movement,
    }

    return render(
        request,
        'cash_register/detail_cash_register.html',
        context
    )
