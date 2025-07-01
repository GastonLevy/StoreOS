from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ...models import Supplier, SupplierEntry
from ...forms import EntryPackForm  # Assuming you have an EntryPackForm form
from storeos.decorators import role_required

@role_required('Admin', 'Modificar_Entrada_Grupo_Proveedor')
def entry_pack_update(request, pk):
    """
    Update an existing SupplierEntry instance (entry pack) belonging to the user's company.

    Args:
        request (HttpRequest): The HTTP request object containing POST data if submitted.
        pk (int): Primary key of the SupplierEntry to update.

    Returns:
        HttpResponse: Redirects to the supplier detail page upon successful update,
                        otherwise renders the form with validation errors.

    Raises:
        Http404: If SupplierEntry with the given pk and company does not exist.
    """
    # Get the SupplierEntry object ensuring it belongs to the user's company
    entry_pack = get_object_or_404(SupplierEntry, pk=pk, company=request.user.userprofile.company)

    # If POST, update the object with form data
    if request.method == 'POST':
        form = EntryPackForm(request.POST, instance=entry_pack)
        if form.is_valid():
            form.save()  # Save the form with updated data
            return redirect('supplier-detail', pk=entry_pack.supplier.pk)  # Redirect to supplier detail page
    else:
        # If not POST, show the form with current data
        form = EntryPackForm(instance=entry_pack)

    return render(request, 'suppliers/entry_pack_form.html', {'form': form, 'entry_pack': entry_pack})
