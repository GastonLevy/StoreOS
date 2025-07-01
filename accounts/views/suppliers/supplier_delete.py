from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models import Supplier
from storeos.decorators import role_required

@role_required('Admin', 'Eliminar_Proveedor')
def supplier_delete(request, pk):
    """
    Delete a supplier after confirmation.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the supplier to delete.

    Returns:
        HttpResponseRedirect: Redirects to supplier list on successful deletion.
        HttpResponse: Renders confirmation page if GET request.

    Raises:
        Http404: If supplier does not exist or does not belong to user's company.
    """
    # Get supplier filtered by user's company
    supplier = get_object_or_404(Supplier, pk=pk, company=request.user.userprofile.company)

    # Check if deletion confirmed via POST
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, f'Proveedor "{supplier.name}" eliminado correctamente.')
        return redirect('supplier-list')  # Redirect to supplier list

    # Render delete confirmation page
    return render(request, 'suppliers/supplier_delete.html', {'supplier': supplier})
