from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages

from ...models import Category, Item
from ...forms import ItemForm
from storeos.decorators import role_required


@role_required('Admin', 'Crear_Producto')
def item_create(request):
    """
    Create a new Item linked to the logged-in user's company.
    """

    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.company = user_profile.company

            stockable = form.cleaned_data.get('stockable')
            quantity = form.cleaned_data.get('quantity')

            is_calculated = form.cleaned_data.get('is_calculated')
            percentage = form.cleaned_data.get('percentage')
            cost = form.cleaned_data.get('cost')

            # Validate that if stockable is True, quantity must be 0
            if stockable and quantity != 0:
                form.add_error(
                    'quantity',
                    'La cantidad debe ser 0 cuando el artículo está marcado como sin inventario.'
                )

                messages.error(
                    request,
                    'La cantidad debe ser 0 cuando el artículo está marcado como sin inventario.'
                )

            else:
                # Automatic sale price calculation
                if is_calculated:
                    item.price = cost * (
                        Decimal('1') + (percentage / Decimal('100'))
                    )

                item.save()
                form.save_m2m()

                messages.success(
                    request,
                    'Ítem creado exitosamente'
                )

                return redirect('item-list')

        else:
            messages.error(
                request,
                'Hubo un error al crear el ítem.'
            )

    else:
        form = ItemForm()

    categories = Category.objects.filter(
        company=user_profile.company
    )

    return render(
        request,
        'item/item_form.html',
        {
            'form': form,
            'categories': categories
        }
    )