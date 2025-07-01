from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from ...models import Person
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Detalle_Cuenta')
def account_detail(request, pk):
    """
    Display detailed information about a Person, including paginated debts and total balance.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Person to retrieve.

    Returns:
        HttpResponse: Rendered template with person details, paginated debts, and balance.

    Raises:
        Http404: If the Person does not belong to the same company as the requesting user.
    """
    person = get_object_or_404(Person, pk=pk)

    # Verify the person belongs to the same company as the logged-in user
    if person.company != request.user.userprofile.company:
        raise Http404("No tienes permiso para ver los detalles de esta persona.")

    # Get debts associated with this person
    debts = person.debts.all()
    balance = person.total_debt()

    # Pagination
    entries_per_page = request.GET.get('entries', 10)
    try:
        entries_per_page = int(entries_per_page)
    except ValueError:
        entries_per_page = 10
    entries_per_page = max(1, min(entries_per_page, 100))  # Allowed range 1-100

    paginator = Paginator(debts, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/account_detail.html', {
        'person': person,
        'balance': balance,
        'page_obj': page_obj,
    })
