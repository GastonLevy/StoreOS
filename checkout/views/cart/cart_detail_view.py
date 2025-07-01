from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import Item
from ...forms import CartLineForm, TemporaryProductForm
from ...models import Cart, CartLine, PaymentMethod
from accounts.models import Person
from django.http import HttpResponse
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Detalle_Carro')
def cart_detail(request, cart_id):
    """
    Display and manage the details of a cart, including adding items (normal, temporary, or with deferred price).

    Args:
        request (HttpRequest): The HTTP request object.
        cart_id (int): The ID of the cart to show or modify.

    Returns:
        HttpResponse: Renders the cart detail page or returns error HTTP responses on invalid data.

    Raises:
        Http404: If the cart does not exist or the user does not have access.
    """
    # Check if the user is superuser or belongs to 'Admin' group
    if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
        # No user filter if admin or superuser
        cart = get_object_or_404(Cart, id=cart_id, company=request.user.userprofile.company)
    else:
        # Filter cart by user
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    cart_lines = cart.cart_lines.all()
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    company = request.user.userprofile.company
    persons = Person.objects.filter(company=company)

    if request.method == 'POST':
        hide = request.POST.get('hide', 'false')
        deferred_price = request.POST.get('deferred_price', 'false')

        print(request.POST)

        # Handle temporary product
        if hide == 'true':
            temp_form = TemporaryProductForm(request.POST)
            if temp_form.is_valid():
                temp_name = temp_form.cleaned_data['temp_name']
                temp_price = temp_form.cleaned_data['temp_price']
                temp_quantity = temp_form.cleaned_data['temp_quantity']

                # Create temporary item
                temp_item = Item.objects.create(
                    name=temp_name,
                    price=temp_price,
                    quantity=0,
                    stockable=False,
                    description="Producto Temporal",
                    company=company
                )

                # Create cart line for temporary product
                cart_line = CartLine(
                    cart=cart,
                    item=temp_item,
                    quantity=temp_quantity,
                    company=company,
                )
                cart_line.save()

                # Delete temporary product after use
                temp_item.delete()

                return redirect('cart-detail', cart_id=cart.id)
            else:
                print("Temporary product form errors:", temp_form.errors)
                return HttpResponse("Error en el formulario del producto temporal.", status=400)

        # Handle deferred price
        elif deferred_price == 'true':
            item_id = request.POST.get('item_id')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')

            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                return HttpResponse("Producto no encontrado.", status=400)

            # Basic validations
            try:
                price = float(price)
                quantity = int(quantity)
            except (ValueError, TypeError):
                return HttpResponse("Precio o cantidad inválidos.", status=400)

            if price <= 0 or quantity <= 0:
                return HttpResponse("Precio y cantidad deben ser mayores que cero.", status=400)

            # Create cart line with custom price
            cart_line = CartLine(
                cart=cart,
                item=item,
                quantity=quantity,
                price=price,  # Override price
                company=company,
            )
            cart_line.save()
            return redirect('cart-detail', cart_id=cart.id)

        else:
            # Process normal form
            form = CartLineForm(request.POST)
            if form.is_valid():
                item_id = form.cleaned_data['item_id']
                try:
                    item = Item.objects.get(id=item_id)
                except Item.DoesNotExist:
                    return HttpResponse("Producto no encontrado.", status=400)

                # Create cart line with item and quantity
                cart_line = CartLine(
                    cart=cart,
                    item=item,
                    quantity=form.cleaned_data['quantity'],
                    company=company,
                )
                cart_line.save()
                return redirect('cart-detail', cart_id=cart.id)
            else:
                print("Form errors:", form.errors)
                return HttpResponse("Error en el formulario de la línea del carrito.", status=400)
    else:
        item_id = request.GET.get('item_id') or request.POST.get('item_id')

        # If valid item_id, load the Item
        if item_id:
            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                item = None
        else:
            item = None

        form = CartLineForm(initial={'quantity': 1, 'item_id': item.id if item else None})

    total_general = sum(line.total for line in cart_lines)

    return render(request, 'checkout/cart_detail.html', {
        'form': form,
        'cart_lines': cart_lines,
        'cart': cart,
        'total_general': total_general,
        'payment_methods': payment_methods,
        'persons': persons,
    })
