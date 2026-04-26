from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from datetime import datetime

from ...models import Cart, PaymentMethod
from storeos.decorators import role_required


@role_required('Admin', 'Cajero', 'Listar_Carro')
@login_required
def cart_list(request):
    company = request.user.userprofile.company

    selected_user = request.GET.get('user', '').strip()
    selected_payment_method = request.GET.get('payment_method', '').strip()
    date_query = request.GET.get('date', '').strip()

    carts = Cart.objects.filter(company=company)

    if selected_user:
        carts = carts.filter(user_id=selected_user)

    if selected_payment_method:
        carts = carts.filter(payment_method_id=selected_payment_method)

    if date_query:
        try:
            date_obj = datetime.strptime(date_query, '%Y-%m-%d')
            carts = carts.filter(created_at__date=date_obj.date())
        except ValueError:
            pass

    carts = carts.order_by('-created_at')

    users = get_user_model().objects.filter(
        userprofile__company=company
    ).order_by('username')

    payment_methods = PaymentMethod.objects.all().order_by('name')

    return render(request, 'checkout/cart_list.html', {
        'carts': carts,
        'page_obj': carts,
        'users': users,
        'payment_methods': payment_methods,
        'selected_user': selected_user,
        'selected_payment_method': selected_payment_method,
        'date_query': date_query,
    })