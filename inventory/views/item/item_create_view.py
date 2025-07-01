from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from ...models import Category, Item
from ...forms import ItemForm
from storeos.decorators import role_required

@role_required('Admin', 'Crear_Producto')
def item_create(request):
    """
    Create a new Item linked to the logged-in user's company.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to item list on success or renders form with errors.

    Raises:
        ValidationError: If 'stockable' is True but 'quantity' is not 0.
    """
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.company = user_profile.company

            # Additional validation for 'stockable' and 'quantity'
            stockable = form.cleaned_data.get('stockable')
            quantity = form.cleaned_data.get('quantity')

            # Validate that if stockable is True, quantity must be 0
            if stockable and quantity != 0:
                form.add_error('quantity', 'La cantidad debe ser 0 cuando el artículo está marcado como sin inventario.')
                messages.error(request, 'La cantidad debe ser 0 cuando el artículo está marcado como sin inventario.')
            else:
                item.save()  # Save the item only if validation passes

                form.save_m2m()  # Save many-to-many categories
                messages.success(request, 'Ítem creado exitosamente')
                return redirect('item-list')
        else:
            messages.error(request, 'Hubo un error al crear el ítem.')

    else:
        form = ItemForm()

    categories = Category.objects.filter(company=user_profile.company)
    return render(request, 'item/item_form.html', {'form': form, 'categories': categories})
