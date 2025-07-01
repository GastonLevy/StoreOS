from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models.cash_register_model import CashRegister
from ..models.cash_register_movement_model import CashMovement
from checkout.models import Cart, CartLine
from django.contrib.auth.models import Group
from django.db.models import Sum
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Detalle_Caja')
def cash_register_detail_view(request, pk):
    """
    Display detailed information of a specific cash register including sales, returns, 
    cash payments, income, expenses, balance, and payment method summaries.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the CashRegister to display.

    Returns:
        HttpResponse: Rendered template with cash register detail context.

    Raises:
        Http404: If the CashRegister does not exist or is not accessible by the user.
    """
    is_admin_or_superadmin = request.user.is_superuser or Group.objects.filter(name='Admin', user=request.user).exists()

    if is_admin_or_superadmin:
        cash_register = get_object_or_404(CashRegister, pk=pk, company=request.user.userprofile.company)
    else:
        cash_register = get_object_or_404(CashRegister, pk=pk, user=request.user)
    
    # Sales: total of completed carts
    ingresos = sum(cart.total_price() for cart in cash_register.carts.filter(is_completed=True))
    
    # Change returned: sum of `payment_return` for carts paid in cash
    vueltos = sum(cart.payment_return or 0 for cart in cash_register.carts.filter(payment_method__name='Efectivo', is_completed=True))
    
    # Sum of paid_amount for carts paid in cash
    efectivo_ingresos = sum(cart.paid_amount or 0 for cart in cash_register.carts.filter(payment_method__name='Efectivo', is_completed=True))
    
    # Income and expenses from cash register movements
    total_ingresos = sum(m.amount for m in cash_register.movements.filter(type='ingreso'))
    total_egresos = sum(m.amount for m in cash_register.movements.filter(type='egreso'))
    
    # Calculate the final balance of cash movements
    movimientos = total_ingresos - total_egresos

    # Calculate final balance: opening balance + cash income - returned change + cash movements in + cash movements out
    balance_total = cash_register.opening_balance + efectivo_ingresos - vueltos + total_ingresos - total_egresos
    
    # Income grouped by payment method
    payment_method_totals = (
        cash_register.carts.filter(is_completed=True)
        .values('payment_method__name')
        .annotate(total=Sum('cart_lines__quantity'))  # Initial total: sum of quantities (will recalc below)
        .order_by('-total')
    )

    # Manually calculate total amount per payment method (quantity * price)
    for payment in payment_method_totals:
        if payment['payment_method__name'] is None:
            payment['payment_method__name'] = 'Sin método de pago'

        total_price = 0
        for cart in cash_register.carts.filter(payment_method__name=payment['payment_method__name'], is_completed=True):
            total_price += sum(line.quantity * line.price for line in cart.cart_lines.all())
        
        payment['total'] = total_price

    # Total quantity moved per item in completed carts
    item_movement = CartLine.objects.filter(
        cart__in=cash_register.carts.filter(is_completed=True)
    ).values('name').annotate(total_quantity=Sum('quantity'))

    context = {
        'cash_register': cash_register,
        'ingresos': ingresos,              # Total sales
        'vueltos': vueltos,                # Total change returned
        'total_ingresos': total_ingresos,  # Total registered incomes
        'total_egresos': total_egresos,    # Total registered expenses
        'movimientos': movimientos,        # Total registered movements
        'balance_total': balance_total,    # Calculated final balance
        'payment_method_totals': payment_method_totals,
        'efectivo_ingresos': efectivo_ingresos,  # Cash payments total
        'lista_movimientos': item_movement,
    }
    return render(request, 'cash_register/detail_cash_register.html', context)
