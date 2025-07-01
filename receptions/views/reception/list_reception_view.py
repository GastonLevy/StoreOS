from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q  # Import Q for filter combinations
from ...models import Reception
from accounts.models import Person
from django.contrib.auth.decorators import login_required
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Listar_Recepcion')
def reception_list(request):
    """
    View to list receptions filtered by company and optional search query, with pagination.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with a paginated list of receptions.

    Raises:
        ValueError: If 'entries' parameter cannot be converted to int.
    """
    search_query = request.GET.get('search', '')  # Get search term from URL
    
    # Filter receptions by user's company
    receptions = Reception.objects.filter(company=request.user.userprofile.company)
    
    if search_query:
        # Use Q objects to combine filters for searching by various fields
        receptions = receptions.filter(
            Q(item__icontains=search_query) |      # Search by item name
            Q(person__first_name__icontains=search_query) |  # Search by person's first name
            Q(person__last_name__icontains=search_query) |   # Search by person's last name
            Q(auth_code__icontains=search_query)   # Search by authenticity code
        )
    
    # Order results by reception date descending (assumes field 'reception_date' exists)
    receptions = receptions.order_by('-reception_date')
    
    # Pagination
    try:
        entries_per_page = int(request.GET.get('entries', 10))  # Default 10 entries per page
    except ValueError:
        entries_per_page = 10  # fallback if invalid value passed

    paginator = Paginator(receptions, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Render the template with paginated results
    return render(request, 'reception/list_reception.html', {
        'page_obj': page_obj,
        'entries_per_page': entries_per_page,
        'search_query': search_query
    })
