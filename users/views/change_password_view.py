from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def cambiar_password(request):
    """
    Allows the user to change their password.
    If the change is successful, the session is logged out and redirected to login.
    """
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña cambiada exitosamente. Por favor, inicia sesión nuevamente.')
            logout(request)
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # Show empty form on first access
        form = PasswordChangeForm(user=request.user)

    return render(request, 'password_change.html', {'form': form})
