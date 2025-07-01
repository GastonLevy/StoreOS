from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from ...models import Debt
from storeos.decorators import role_required

@role_required('Admin', 'Eliminar_Deuda')
def debt_delete(request, pk):
    """
    Delete a Debt instance if it belongs to the logged-in user's company.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Debt to delete.

    Returns:
        HttpResponse: Redirects to the associated person's account detail upon successful deletion,
                        or renders the confirmation page if GET request.

    Raises:
        Http404: If the debt is not associated with the user's company.
    """
    debt = get_object_or_404(Debt, pk=pk)

    # Check if the debt belongs to the same company as the logged-in user
    if debt.person.company != request.user.userprofile.company:
        raise Http404("No tienes permiso para eliminar esta deuda.")

    if request.method == 'POST':
        # Delete the debt on form submission
        debt.delete()
        return redirect('account-detail', pk=debt.person.id)

    # Render confirmation page for GET requests
    return render(request, 'accounts/account_debt_delete.html', {'debt': debt})
