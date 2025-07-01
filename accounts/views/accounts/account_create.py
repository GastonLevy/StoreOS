from django.shortcuts import render, redirect
from ...forms import PersonForm
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Crear_Cuenta')
def account_create(request):
    """
    Create a new Person account associated with the user's company.

    Args:
        request (HttpRequest): The HTTP request object, expects POST data with PersonForm fields.

    Returns:
        HttpResponse: Renders the account creation form on GET or invalid POST.
        HttpResponseRedirect: Redirects to account list on successful creation.

    Raises:
        None explicitly.
    """
    # Process form on POST
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            # Assign the company to the logged-in user's company
            person.company = request.user.userprofile.company
            person.save()
            return redirect('account-list')
    else:
        # Show empty form on GET
        form = PersonForm()
    return render(request, 'accounts/account_form.html', {'form': form})
