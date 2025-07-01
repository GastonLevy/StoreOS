from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ...models import Supplier
from ...forms import SupplierForm
from storeos.decorators import role_required

@role_required('Admin', 'Crear_Proveedor')
def supplier_create(request):
    """
    Create a new supplier associated with the user's company.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to supplier list after successful creation.
        HttpResponse: Renders supplier creation form if GET or invalid POST.

    Raises:
        None
    """
    # Handle POST request to create supplier
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            # Associate supplier with the user's company
            supplier.company = request.user.userprofile.company
            supplier.save()
            return redirect('supplier-list')  # Redirect to supplier list
    else:
        # Initialize empty form for GET request
        form = SupplierForm()

    return render(request, 'suppliers/supplier_form.html', {'form': form})
