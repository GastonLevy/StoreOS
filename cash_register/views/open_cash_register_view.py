from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import OpenCashRegisterForm
from ..models.cash_register_model import CashRegister
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Abrir_Caja')
def open_cash_register_view(request):
    """
    Handle opening a cash register for the current user and company.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to cash register detail if already open,
                      otherwise renders the open cash register form.
    
    Raises:
        None explicitly, but form validation errors may occur.
    """
    user = request.user
    company = user.userprofile.company

    # Check if there's already an open cash register for this user
    cash_register = CashRegister.objects.filter(user=user, status='abierta').first()
    if cash_register:
        # If an open cash register exists, redirect to its detail page
        return redirect('cash-register-detail', pk=cash_register.pk)

    if request.method == 'POST':
        form = OpenCashRegisterForm(request.POST, user=user)
        if form.is_valid():
            # Create and save the cash register
            cash_register = form.save(commit=False)
            cash_register.user = user
            cash_register.company = company
            cash_register.status = 'abierta'
            cash_register.save()
            messages.success(request, "Caja abierta correctamente.")
            return redirect('cart-create')
    else:
        form = OpenCashRegisterForm(user=user)

    return render(request, 'cash_register/open_cash_register.html', {'form': form})
