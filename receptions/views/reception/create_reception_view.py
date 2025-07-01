from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...forms import ReceptionForm
from ...models import Reception
from accounts.models import Person
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Crear_Recepcion')
def reception_create(request):
    """
    Create a new Reception entry.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered form page or redirect on success.

    Raises:
        None explicitly, but redirects if no company associated with user.
    """
    user_profile = request.user.userprofile  # Get the user's profile

    if not user_profile.company:
        messages.error(request, 'Debes asociar una compañía a tu perfil antes de crear una recepción.')
        return redirect('profile')  # Redirect to profile to associate company

    if request.method == 'POST':
        form = ReceptionForm(request.POST, user_profile=user_profile)  # Pass user_profile to form

        # Only access cleaned_data if form is valid
        if form.is_valid():
            reception = form.save(commit=False)
            reception.received_by = request.user  # Assign current user
            reception.company = user_profile.company  # Assign company to reception

            # Get person (new or existing) from form data
            reception.person = form.cleaned_data.get('person')  
            reception.save()

            messages.success(request, 'Recepción creada exitosamente')
            return redirect('reception-list')  # Redirect to reception list
        else:
            messages.error(request, 'Hubo un error al crear la recepción. Verifica los datos.')

    else:
        form = ReceptionForm(user_profile=user_profile)  # Pass user_profile to form

    # Get persons list for dropdown
    persons = Person.objects.filter(company=user_profile.company)

    return render(request, 'reception/create_reception.html', {'form': form, 'persons': persons})
