from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ...models import Item, Category
from ...forms import ItemForm
from storeos.decorators import role_required

@role_required('Admin', 'Modificar_Producto')
def item_update(request, pk):
    """
    Update an existing item associated with the user's company.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Item to update.

    Returns:
        HttpResponse: Rendered template response or redirect.

    Raises:
        Http404: If the item with the given pk and company does not exist.
    """
    user_profile = request.user.userprofile
    item = get_object_or_404(Item, pk=pk, company=user_profile.company)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)  # Load form with item instance for editing

        if form.is_valid():
            # Validation for stockable and quantity
            stockable = form.cleaned_data.get('stockable')
            quantity = form.cleaned_data.get('quantity')

            # If item is stockable but quantity is not zero, show error
            if stockable and quantity != 0:
                messages.error(request, 'La cantidad debe ser 0 cuando el artículo está marcado como sin inventario.')
                categories = Category.objects.filter(company=user_profile.company)
                return render(request, 'item/item_form.html', {'form': form, 'categories': categories})

            form.save()  # Save the valid form

            messages.success(request, 'Ítem actualizado exitosamente')
            return redirect('item-detail', pk=item.pk)
        else:
            # Form has errors
            messages.error(request, 'Hubo un error al actualizar el ítem.')
            print(form.errors)  # Debug print

    else:
        form = ItemForm(instance=item)  # Populate form with existing item data

    categories = Category.objects.filter(company=user_profile.company)  # Get categories for the company

    return render(request, 'item/item_form.html', {'item': item, 'categories': categories, 'form': form})
