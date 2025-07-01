from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models import Person
from storeos.decorators import role_required

@role_required('Admin', 'Eliminar_Cuenta')
def account_delete(request, pk):
    """
    Handle the deletion of a Person account after confirmation.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Person to delete.

    Returns:
        HttpResponse: Redirects to the account list on successful deletion,
                        or renders the confirmation page if GET request.

    Raises:
        Http404: If the Person does not belong to the user's company or does not exist.
    """
    user_company = request.user.userprofile.company

    # Retrieve the Person belonging to the user's company or raise 404
    person = get_object_or_404(Person, pk=pk, company=user_company)

    if request.method == 'POST':
        # Delete the Person and show success message
        person.delete()
        messages.success(request, 'La persona ha sido eliminada correctamente.')
        return redirect('account-list')

    # Render confirmation page on GET request
    return render(request, 'accounts/account_delete.html', {'person': person})
