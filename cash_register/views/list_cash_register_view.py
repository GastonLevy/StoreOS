from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.cash_register_model import CashRegister
from django.core.paginator import Paginator
from storeos.decorators import role_required

@role_required('Admin', 'Listar_Caja')
def cash_register_list_view(request):
    """
    Display a paginated list of cash registers for the user's company, with optional search.

    Args:
        request (HttpRequest): The HTTP request object containing GET parameters:
            - 'search' (str, optional): Filter cash registers by user username (case-insensitive).
            - 'entries' (int, optional): Number of entries per page (default 10, max 100).
            - 'page' (int, optional): Page number for pagination (default 1).

    Returns:
        HttpResponse: Rendered template with paginated cash register list.

    Raises:
        None explicitly, but invalid 'entries' and 'page' parameters are handled gracefully.
    """
    user_profile = request.user.userprofile

    # Get cash registers filtered by user's company, ordered by creation date descending
    cash_registers = CashRegister.objects.filter(company=user_profile.company).order_by('-created_at')

    # Get the search term from request (if any)
    search_query = request.GET.get('search', '').strip()

    if search_query:
        # Filter cash registers by username containing the search term (case-insensitive)
        cash_registers = cash_registers.filter(user__username__icontains=search_query)

    # Get number of entries per page from request, default 10
    entries_per_page = request.GET.get('entries', 10)
    try:
        entries_per_page = int(entries_per_page)  # Ensure it's an integer
    except ValueError:
        entries_per_page = 10  # Default if invalid input

    # Limit entries per page between 1 and 100 to avoid excessive range
    if entries_per_page < 1:
        entries_per_page = 10
    elif entries_per_page > 100:
        entries_per_page = 100

    # Set up paginator and get requested page
    paginator = Paginator(cash_registers, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Context for rendering template
    context = {
        'page_obj': page_obj,
        'entries_per_page': entries_per_page,
        'search_query': search_query,  # Pass search term back to template
    }

    return render(request, 'cash_register/list_cash_register.html', context)
