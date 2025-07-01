from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import models  # For using Q in queries
from storeos.decorators import role_required
from ...models import Supplier

@role_required('Admin', 'Listar_Proveedor')
def supplier_list(request):
    """
    Retrieve and display a paginated list of suppliers filtered by company and optional search query.

    Args:
        request (HttpRequest): The HTTP request object containing GET parameters for search and pagination.

    Returns:
        HttpResponse: Rendered template with paginated suppliers list.

    Raises:
        None
    """
    # Get suppliers belonging to the user's company
    suppliers = Supplier.objects.filter(company=request.user.userprofile.company)
    
    # Get the search term from query parameters
    search_query = request.GET.get('search', '').strip()
    if search_query:
        suppliers = suppliers.filter(
            models.Q(name__icontains=search_query) | 
            models.Q(email__icontains=search_query)
        )
    
    # Pagination: entries per page
    entries_per_page = int(request.GET.get('entries', 10))  # Default: 10 entries per page
    paginator = Paginator(suppliers, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'suppliers/supplier_list.html',
        {
            'page_obj': page_obj,
            'entries_per_page': entries_per_page,
            'search_query': search_query  # Send search term to template
        }
    )
