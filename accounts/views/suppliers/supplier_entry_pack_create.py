from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from ...models import Supplier, EntryPack, SupplierEntry
from storeos.decorators import role_required

@role_required('Admin', 'Crear_Entrada_Grupo_Proveedor')
def entrypack_create(request, supplier_id):
    """
    Create a new EntryPack for a given supplier within the user's company.

    Args:
        request (HttpRequest): The HTTP request object.
        supplier_id (int): ID of the supplier to link the EntryPack.

    Returns:
        HttpResponse: Redirects to the supplier detail page on successful creation,
                      or renders the creation form otherwise.

    Raises:
        Http404: If the supplier or any referenced SupplierEntry does not exist.
    """
    # Check supplier exists or 404
    supplier = get_object_or_404(Supplier, id=supplier_id)
    
    # Check supplier belongs to the same company as the current user
    if supplier.company != request.user.userprofile.company:
        return redirect('supplier-list')  # Redirect if company mismatch
    
    if request.method == 'POST':
        # Create the EntryPack object
        description = request.POST.get('description', '')
        entry_pack = EntryPack.objects.create(
            supplier=supplier,
            description=description,
            company=request.user.userprofile.company
        )
        
        # If there are SupplierEntry IDs, link them to the EntryPack
        entries = request.POST.getlist('entries')  # Expecting a list of SupplierEntry IDs
        for entry_id in entries:
            entry = get_object_or_404(SupplierEntry, id=entry_id)
            entry_pack.entries.add(entry)
        
        entry_pack.save()

        return redirect('supplier-detail', pk=supplier.id)
    
    # Render form if GET or other methods
    return render(request, 'create_entrypack.html', {'supplier': supplier})
