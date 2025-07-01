from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ...models import Supplier
from ...forms import SupplierForm
from storeos.decorators import role_required

@role_required('Admin', 'Modificar_Proveedor')
def supplier_update(request, pk):
    """
    Update an existing supplier instance.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the supplier to update.

    Returns:
        HttpResponse: Rendered template with form or a redirect response.

    Raises:
        Http404: If the supplier does not exist or does not belong to user's company.
    """
    # Ensure the supplier belongs to the same company as the user
    supplier = get_object_or_404(Supplier, pk=pk, company=request.user.userprofile.company)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()  # Save changes to the existing supplier
            return redirect('supplier-list')  # Redirect to supplier list
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'suppliers/supplier_form.html', {'form': form, 'supplier': supplier})
