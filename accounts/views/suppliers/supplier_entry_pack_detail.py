from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from ...models import EntryPack
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from storeos.decorators import role_required

@role_required('Admin', 'Detalle_Entrada_Grupo_Proveedor')
def entry_pack_detail(request, entry_pack_id):
    """
    Display the details of a specific EntryPack, including its entries with pagination.

    Args:
        request (HttpRequest): The HTTP request object.
        entry_pack_id (int): The ID of the EntryPack to display.

    Returns:
        HttpResponse: Rendered page with EntryPack details and paginated entries.

    Raises:
        HttpResponseForbidden: If the EntryPack does not belong to the user's company.
        Http404: If EntryPack with given ID does not exist.
    """
    # Get the EntryPack object by ID or return 404 if not found
    entry_pack = get_object_or_404(EntryPack, id=entry_pack_id)
    
    # Check if the EntryPack belongs to the user's company
    if entry_pack.company != request.user.userprofile.company:
        messages.error(request, "No tienes permisos para ver este pack de entradas.")
        return HttpResponseForbidden()
    
    # Get all entries related to this EntryPack
    entries = entry_pack.entries.all()

    # Setup pagination: 10 entries per page
    paginator = Paginator(entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the detail template with paginated entries
    return render(request, 'suppliers/supplier_entry_pack_detail.html', {
        'entry_pack': entry_pack,
        'page_obj': page_obj,
        'supplier_id': entry_pack.supplier.id,
        'entry_pack_id': entry_pack.id,
    })
