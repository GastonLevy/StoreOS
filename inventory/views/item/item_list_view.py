from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from ...models import Item
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Listar_Producto')
def item_list(request):
    """
    List items belonging to the user's company with optional search and pagination.

    Args:
        request (HttpRequest): The HTTP request containing optional GET parameters:
            - 'search' (str): Search query to filter items by name or barcode.
            - 'entries' (int): Number of items per page (default 10, max 100).
            - 'page' (int): Page number for pagination.

    Returns:
        HttpResponse: Rendered HTML page with paginated and filtered item list.

    Raises:
        None
    """
    user_profile = request.user.userprofile
    # Get all items of the user's company
    items = Item.objects.filter(company=user_profile.company)

    # Get search query string from request (default empty)
    search_query = request.GET.get('search', '').strip()

    if search_query:
        # Filter items by name or barcode containing search term (case-insensitive)
        items = items.filter(name__icontains=search_query) | items.filter(barcode__icontains=search_query)

    # Get number of entries per page (default 10)
    entries_per_page = request.GET.get('entries', 10)
    try:
        entries_per_page = int(entries_per_page)  # Ensure it is an integer
    except ValueError:
        entries_per_page = 10

    # Limit entries_per_page to reasonable range to avoid abuse
    if entries_per_page < 1:
        entries_per_page = 10
    elif entries_per_page > 100:
        entries_per_page = 100

    # Set up paginator
    paginator = Paginator(items, entries_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Return view with filtered items and pagination info
    return render(request, 'item/item_list.html', {
        'page_obj': page_obj,
        'entries_per_page': entries_per_page,
        'search_query': search_query  # Pass search query to template
    })
