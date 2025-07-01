from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ...models import Item
from accounts.models import SupplierEntry
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Detalle_Producto')
def item_detail(request, pk):
    """
    Display item details along with paginated supplier entries filtered by the user's company.

    Args:
        request (HttpRequest): The HTTP request containing optional GET parameters:
            - 'entries' (int): Number of entries per page (default 10).
            - 'page' (int): Page number for pagination (default 1).
        pk (int): Primary key of the Item to retrieve.

    Returns:
        HttpResponse: Rendered HTML page showing item details and paginated supplier entries.

    Raises:
        Http404: If the item does not exist or does not belong to the user's company.
    """
    # Get user's company
    company = request.user.userprofile.company

    # Retrieve the item, ensuring it belongs to the user's company
    item = get_object_or_404(Item, pk=pk, company=company)

    # Get number of entries per page (default 10)
    try:
        entries_per_page = int(request.GET.get('entries', 10))
    except ValueError:
        entries_per_page = 10

    # Get current page number (default 1)
    page_number = request.GET.get('page', 1)

    # Paginate supplier entries for this item filtered by company, ordered by id
    entries = SupplierEntry.objects.filter(item=item, company=company).order_by('id')
    paginator = Paginator(entries, entries_per_page)

    # Get requested page
    page_obj = paginator.get_page(page_number)

    # Render template with item and paginated entries
    return render(
        request,
        'item/item_detail.html',
        {
            'item': item,
            'page_obj': page_obj,  # Current page of entries
            'entries_per_page': entries_per_page  # Number of entries per page
        }
    )
