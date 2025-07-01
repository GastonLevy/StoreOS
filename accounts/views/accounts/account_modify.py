from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from ...models import Person
from ...forms import PersonForm
from storeos.decorators import role_required

@role_required('Admin', 'Modificar_Cuenta')
def account_update(request, pk):
    """
    Update a Person's account if the person belongs to the user's company.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Person to update.

    Returns:
        HttpResponseRedirect: Redirects to account list on successful update.
        HttpResponse: Renders the form for editing if GET or invalid POST.

    Raises:
        Http404: If the Person does not belong to the user's company or does not exist.
    """
    # Retrieve person by pk or raise 404
    person = get_object_or_404(Person, pk=pk)

    # Check that person belongs to user's company for permission
    if person.company != request.user.userprofile.company:
        raise Http404("No tienes permiso para editar esta persona.")

    # Process form on POST request
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('account-list')  # Redirect to person list
    else:
        # Initialize form with instance on GET request
        form = PersonForm(instance=person)

    return render(request, 'accounts/account_form.html', {'form': form, 'person': person})
