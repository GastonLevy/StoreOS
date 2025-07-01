from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ...models import SupplierEntry, Supplier, EntryPack
from inventory.models import Item
from storeos.decorators import role_required

@role_required('Admin', 'Eliminar_Entrada_Proveedor')
def supplier_entry_delete_confirm(request, pk, entry_pack_id):
    """
    Confirm and process the deletion of a SupplierEntry.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the SupplierEntry to delete.
        entry_pack_id (int): Primary key of the related EntryPack.

    Returns:
        HttpResponse: Renders the confirmation page or redirects after deletion.
        HttpResponseForbidden: If the SupplierEntry or EntryPack does not belong to the user's company.

    Raises:
        Http404: If SupplierEntry or EntryPack does not exist.
    """
    supplier_entry = get_object_or_404(SupplierEntry, pk=pk)
    entry_pack = get_object_or_404(EntryPack, pk=entry_pack_id)
    user_company = request.user.userprofile.company

    # Check if the supplier belongs to the same company as the user
    if supplier_entry.supplier.company != user_company:
        return HttpResponseForbidden("No puedes eliminar entradas de proveedores de otra compañía.")

    if entry_pack.company != user_company:
        return HttpResponseForbidden("No puedes eliminar entradas de proveedores de otra compañía.")

    # If the request method is POST, delete the entry and subtract quantity from the item
    if request.method == 'POST':
        item = supplier_entry.item  # Get the item related to the entry
        if item:
            item.quantity -= supplier_entry.quantity  # Subtract the quantity registered in the entry
            if item.quantity < 0:
                item.quantity = 0  # Prevent negative quantity
            item.save()  # Save changes to the item

        # Remove the SupplierEntry from the EntryPack's entries
        entry_pack.entries.remove(supplier_entry)

        # Delete the SupplierEntry
        supplier_entry.delete()

        # Redirect to the EntryPack detail page
        return redirect('entry-pack-detail', entry_pack_id=entry_pack.id)

    # Render the deletion confirmation page
    return render(request, 'suppliers/supplier_entry_delete.html', {'supplier_entry': supplier_entry})
