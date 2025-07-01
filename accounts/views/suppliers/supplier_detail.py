from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from ...models import Supplier, EntryPack
from storeos.decorators import role_required

@role_required('Admin', 'Detalle_Proveedor')
def supplier_detail(request, pk):
    """
    Display supplier details along with their entry packs, paginated.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the supplier.

    Returns:
        HttpResponse: Renders the supplier detail page with paginated entry packs.

    Raises:
        Http404: If supplier does not exist or does not belong to user's company.
    """
    # Get supplier filtered by company
    supplier = get_object_or_404(Supplier, pk=pk, company=request.user.userprofile.company)

    # Filter entry packs by supplier and company, order by creation date descending
    entry_packs = EntryPack.objects.filter(supplier=supplier, company=request.user.userprofile.company).order_by('-created_at')

    # Pagination setup
    entries_per_page = int(request.GET.get('entries', 10))  # Default 10 entries per page
    paginator = Paginator(entry_packs, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'suppliers/supplier_detail.html',
        {
            'supplier': supplier,
            'page_obj': page_obj,
            'entries_per_page': entries_per_page
        }
    )
