from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from inventory.models import Item
from ...forms import CartLineForm, TemporaryProductForm
from ...models import Cart, CartLine, PaymentMethod
from accounts.models import Person
from storeos.decorators import role_required


@role_required('Admin', 'Cajero', 'Detalle_Carro')
def cart_detail(request, cart_id):
    if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
        cart = get_object_or_404(Cart, id=cart_id, company=request.user.userprofile.company)
    else:
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    cart_lines = cart.cart_lines.all()
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    company = request.user.userprofile.company
    persons = Person.objects.filter(company=company)

    if request.method == 'POST':
        hide = request.POST.get('hide', 'false')
        deferred_price = request.POST.get('deferred_price', 'false')

        if hide == 'true':
            temp_form = TemporaryProductForm(request.POST)

            if temp_form.is_valid():
                temp_name = temp_form.cleaned_data['temp_name']
                temp_price = temp_form.cleaned_data['temp_price']
                temp_quantity = Decimal(str(temp_form.cleaned_data['temp_quantity']))

                temp_item = Item.objects.create(
                    name=temp_name,
                    price=temp_price,
                    quantity=0,
                    stockable=False,
                    description="Producto Temporal",
                    company=company
                )

                CartLine.objects.create(
                    cart=cart,
                    item=temp_item,
                    quantity=temp_quantity,
                    company=company,
                )

                temp_item.delete()

                return redirect('cart-detail', cart_id=cart.id)

            return HttpResponse("Error en el formulario del producto temporal.", status=400)

        elif deferred_price == 'true':
            item_id = request.POST.get('item_id')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')

            try:
                item = Item.objects.get(id=item_id, company=company)
            except Item.DoesNotExist:
                return HttpResponse("Producto no encontrado.", status=400)

            try:
                price = Decimal(str(price))
                quantity = Decimal(str(quantity))
            except Exception:
                return HttpResponse("Precio o cantidad inválidos.", status=400)

            if price <= 0 or quantity <= 0:
                return HttpResponse("Precio y cantidad deben ser mayores que cero.", status=400)

            existing_line = CartLine.objects.filter(
                cart=cart,
                item=item,
                price=price,
                company=company
            ).first()

            if existing_line:
                existing_line.quantity += quantity
                existing_line.save()
            else:
                CartLine.objects.create(
                    cart=cart,
                    item=item,
                    quantity=quantity,
                    price=price,
                    company=company,
                )

            return redirect('cart-detail', cart_id=cart.id)

        form = CartLineForm(request.POST)

        if form.is_valid():
            item_id = form.cleaned_data['item_id']
            quantity = Decimal(str(form.cleaned_data['quantity']))

            try:
                item = Item.objects.get(id=item_id, company=company)
            except Item.DoesNotExist:
                return HttpResponse("Producto no encontrado.", status=400)

            existing_line = CartLine.objects.filter(
                cart=cart,
                item=item,
                company=company
            ).first()

            if existing_line:
                existing_line.quantity += quantity
                existing_line.save()
            else:
                CartLine.objects.create(
                    cart=cart,
                    item=item,
                    quantity=quantity,
                    company=company,
                )

            return redirect('cart-detail', cart_id=cart.id)

        return HttpResponse("Error en el formulario de la línea del carrito.", status=400)

    item_id = request.GET.get('item_id')
    item = None

    if item_id:
        try:
            item = Item.objects.get(id=item_id, company=company)
        except Item.DoesNotExist:
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