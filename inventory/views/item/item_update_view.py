from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ...models import Item, Category
from ...forms import ItemForm
from storeos.decorators import role_required


@role_required('Admin', 'Modificar_Producto')
def item_update(request, pk):
    """
    Update an existing item associated with the user's company.
    """

    user_profile = request.user.userprofile

    item = get_object_or_404(
        Item,
        pk=pk,
        company=user_profile.company
    )

    if request.method == 'POST':
        form = ItemForm(
            request.POST,
            instance=item
        )

        if form.is_valid():
            stockable = form.cleaned_data.get('stockable')
            quantity = form.cleaned_data.get('quantity')

            is_calculated = form.cleaned_data.get('is_calculated')
            percentage = form.cleaned_data.get('percentage')
            cost = form.cleaned_data.get('cost')

            if stockable and quantity != 0:
                messages.error(
                    request,
                    'La cantidad debe ser 0 cuando el artículo está marcado como sin inventario.'
                )

                categories = Category.objects.filter(
                    company=user_profile.company
                )

                return render(
                    request,
                    'item/item_form.html',
                    {
                        'item': item,
                        'form': form,
                        'categories': categories
                    }
                )

            item = form.save(commit=False)

            # Si el producto usa cálculo automático,
            # recalcular siempre el precio usando costo + porcentaje.
            if is_calculated:
                item.price = (
                    cost * (
                        Decimal('1') +
                        (percentage / Decimal('100'))
                    )
                ).quantize(Decimal('0.01'))

            # Si is_calculated es False,
            # dejamos el price enviado manualmente por el formulario.

            item.save()
            form.save_m2m()

            messages.success(
                request,
                'Ítem actualizado exitosamente'
            )

            return redirect(
                'item-detail',
                pk=item.pk
            )

        else:
            messages.error(
                request,
                'Hubo un error al actualizar el ítem.'
            )

    else:
        form = ItemForm(instance=item)

    categories = Category.objects.filter(
        company=user_profile.company
    )

    return render(
        request,
        'item/item_form.html',
        {
            'item': item,
            'categories': categories,
            'form': form
        }
    )