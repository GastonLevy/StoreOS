from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.cash_register_model import CashRegister
from django.contrib.auth.models import Group
from django.utils import timezone
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Cerrar_Caja')
def close_cash_register_view(request, cash_register_pk):
    """
    Close an open cash register and record its closing balance.

    Args:
        request (HttpRequest): The HTTP request object.
        cash_register_pk (int or None): Primary key of the cash register to close. Optional for admin users.

    Returns:
        HttpResponse: Redirects to 'home' after successful closing, or renders closing form.
    
    Raises:
        None explicitly, but if no open cash register is found, user is redirected with an error message.
    """
    user = request.user

    # Check if the user is superuser or belongs to Admin group
    is_admin_or_superadmin = user.is_superuser or Group.objects.filter(name='Admin', user=user).exists()

    # Retrieve the open cash register based on user role and optional pk
    if is_admin_or_superadmin:
        if cash_register_pk:
            cash_register = CashRegister.objects.filter(pk=cash_register_pk, status='abierta', company=user.userprofile.company).first()
        else:
            cash_register = CashRegister.objects.filter(status='abierta', company=user.userprofile.company).first()
    else:
        if cash_register_pk:
            cash_register = CashRegister.objects.filter(pk=cash_register_pk, user=user, status='abierta', company=user.userprofile.company).first()
        else:
            cash_register = CashRegister.objects.filter(user=user, status='abierta', company=user.userprofile.company).first()

    if not cash_register:
        messages.error(request, "No tienes una caja abierta para cerrar.")
        return redirect('cash-register-open')  # Redirect to open cash register page if none open

    if request.method == 'POST':
        # Close the cash register and record the closing balance
        closing_balance = request.POST.get('closing_balance')  # This can be replaced by a form field if desired
        cash_register.closing_balance = closing_balance
        cash_register.status = 'cerrada'
        cash_register.closed_at = timezone.now()
        cash_register.save()

        messages.success(request, "Caja cerrada correctamente.")
        return redirect('home')  # Redirect to home or any desired page after closing

    # On GET, render form with empty closing_balance initial value
    return render(request, 'cash_register/close_cash_register.html', {
        'cash_register': cash_register,
        'closing_balance': ''
    })
