from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from ...models import EntryPack
from django.contrib import messages
from storeos.decorators import role_required

@role_required('Admin', 'Eliminar_Entrada_Grupo_Proveedor')
def entry_pack_delete(request, pk):
    """
    Delete a specific EntryPack belonging to the user's company after confirmation.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the EntryPack to delete.

    Returns:
        HttpResponse: Redirects to supplier detail page on successful deletion,
                        or renders a confirmation page otherwise.

    Raises:
        Http404: If the EntryPack does not exist or does not belong to the user's company.
    """
    # Get the EntryPack or 404 if not found or not belonging to user's company
    entry_pack = get_object_or_404(EntryPack, pk=pk, company=request.user.userprofile.company)
    
    if request.method == "POST":
        # Delete the EntryPack after confirmation
        entry_pack.delete()
        messages.success(request, "Pack eliminado con éxito.")
        return redirect('supplier-detail', pk=entry_pack.supplier.pk)
    
    # Render the confirmation template
    return render(request, 'suppliers/supplier_entry_pack_delete.html', {'entry_pack': entry_pack})
