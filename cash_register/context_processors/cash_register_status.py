from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q
from ..models import CashRegister, CashMovement
from checkout.models import Cart

def cash_register_status(request):
    """
    Check if the authenticated user has an open cash register.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: {'is_cash_register_open': bool} indicating if user has an open cash register.
    """
    if request.user.is_authenticated:
        is_cash_register_open = CashRegister.objects.filter(user=request.user, status='abierta').exists()
    else:
        is_cash_register_open = False
    return {'is_cash_register_open': is_cash_register_open}

def cash_register_amount(request):
    """
    Calculate the current cash amount for the authenticated user's open cash register.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: {'actual_amount': Decimal} representing the current cash amount.

    Raises:
        None explicitly, but relies on database queries that may raise exceptions if database is inaccessible.
    """
    if request.user.is_authenticated:
        company = request.user.userprofile.company
        user = request.user

        # Try to get the user's open cash register for their company
        cash_register = CashRegister.objects.filter(
            user=user, 
            company=company, 
            status='abierta'
        ).first()  # Use first() to avoid exceptions if none found

        if not cash_register:
            return {'actual_amount': 0}  # Return default if no open cash register

        # Get the current uncompleted cart for user and company
        cart = Cart.objects.filter(
            user=user,
            company=company,
            is_completed=False
        ).first()

        # Calculate total change returned and cash payments in completed carts linked to cash_register
        change_returned = sum(
            c.payment_return or 0 for c in cash_register.carts.filter(
                payment_method__name='Efectivo', is_completed=True
            )
        )
        cash_payments = sum(
            c.paid_amount or 0 for c in cash_register.carts.filter(
                payment_method__name='Efectivo', is_completed=True
            )
        )

        # Calculate total balance (opening balance + cash payments - change returned)
        total_balance = cash_register.opening_balance + cash_payments - change_returned

        # Get cash movements (income and expenses) with payment method 'Efectivo'
        cash_movements = CashMovement.objects.filter(
            cash_register=cash_register,
            payment_method__name='Efectivo'
        )
        
        # Aggregate sum of incomes and expenses
        movements_balance = cash_movements.aggregate(
            total_ingresos=Sum('amount', filter=Q(type='ingreso')),
            total_egresos=Sum('amount', filter=Q(type='egreso'))
        )

        # Adjust total balance by adding incomes and subtracting expenses
        total_balance += movements_balance['total_ingresos'] or 0
        total_balance -= movements_balance['total_egresos'] or 0

        return {'actual_amount': total_balance}
    else:
        return {'actual_amount': 0}  # Default if not authenticated
