from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

# View to log out the currently authenticated user
@login_required
def logout_view(request):
    """
    Logs out the currently authenticated user and redirects to the login view.
    """
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login')
