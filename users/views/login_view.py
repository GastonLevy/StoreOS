from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    """
    Login view. Authenticates the user and redirects if valid.
    """
    # If the user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Check if fields are not empty
        if not username or not password:
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to category list after successful login
            return redirect('category-list')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')
