from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db import transaction
from ...models import SupplierEntry, Supplier, EntryPack
from inventory.models import Item
from storeos.decorators import role_required

@role_required('Admin', 'Crear_Entrada_Proveedor')
def create_supplier_entry(request):
    """
    Create a SupplierEntry associated with a supplier, item, and entry pack.

    Args:
        request (HttpRequest): The HTTP request object containing POST data.

    Returns:
        HttpResponseRedirect: Redirects to 'entry-pack-detail' on success,
                              or 'supplier-detail' on failure or invalid data.
        HttpResponseForbidden: If supplier, item, or entry pack does not belong to user's company.

    Raises:
        Http404: If supplier, item, or entry pack does not exist.
    """
    user_company = request.user.userprofile.company

    # Get supplier from POST data
    supplier_id = request.POST.get('supplier')
    supplier = get_object_or_404(Supplier, id=supplier_id)

    # Check supplier company matches user's company
    if supplier.company != user_company:
        return HttpResponseForbidden("No puedes crear entradas para proveedores de otra compañía.")

    # Only process POST requests
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')
        comment = request.POST.get('comment') or ""
        expiration_date = request.POST.get('expiration_date')  # Expiration date
        cost = request.POST.get('cost')  # Cost
        entry_pack_id = request.POST.get('entry_pack_id')

        # Validate quantity (must be positive integer)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except (ValueError, TypeError):
            messages.error(request, "Cantidad inválida.")
            return redirect('supplier-detail', pk=supplier.id)

        # Validate cost (must be float)
        try:
            cost = float(cost)
        except (ValueError, TypeError):
            messages.error(request, "Costo inválido.")
            return redirect('supplier-detail', pk=supplier.id)

        # Get item and check company
        item = get_object_or_404(Item, id=item_id)
        if item.company != user_company:
            return HttpResponseForbidden("No puedes registrar entradas con ítems de otra compañía.")

        # Get EntryPack and check company
        entry_pack = get_object_or_404(EntryPack, id=entry_pack_id)
        if entry_pack.company != user_company:
            return HttpResponseForbidden("No puedes agregar entradas a packs de otra compañía.")

        # Use transaction to ensure atomicity
        try:
            with transaction.atomic():
                # Create SupplierEntry with expiration date and cost
                supplier_entry = SupplierEntry.objects.create(
                    supplier=supplier,
                    item=item,
                    item_name=item.name,
                    item_code=item.barcode,
                    quantity=quantity,
                    comment=comment,
                    expiration_date=expiration_date,
                    cost=cost,
                    company=user_company
                )

                # Add SupplierEntry to EntryPack
                entry_pack.entries.add(supplier_entry)

                # Update item quantity
                item.quantity += quantity
                item.save()

            # Redirect to entry pack detail on success
            return redirect('entry-pack-detail', entry_pack_id=entry_pack.id)

        except Exception as e:
            messages.error(request, f"Error al crear o agregar SupplierEntry: {e}")
            return redirect('supplier-detail', pk=supplier.id)

    # If not POST, redirect to supplier detail
    return redirect('supplier-detail', pk=supplier.id)
