from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db import IntegrityError
from ..models import Company, UserProfile

# Decorator to allow access only to admin users
def admin_required(user):
    return user.is_superuser

@user_passes_test(admin_required)
def register_view(request):
    """
    Allows the superuser to register a new user and assign them to a company.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        company_id = request.POST.get('company')

        if not username or not password or not password_confirm or not company_id:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('register')

        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')

        try:
            # Ensure the company exists
            company = Company.objects.get(id=company_id)

            user = User.objects.create_user(username=username, password=password)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.company = company
            profile.save()

            return redirect('home')
        except Company.DoesNotExist:
            messages.error(request, 'La empresa seleccionada no existe.')
        except IntegrityError:
            messages.error(request, 'El nombre de usuario ya está en uso')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')

    companies = Company.objects.all()
    return render(request, 'register.html', {'companies': companies})
