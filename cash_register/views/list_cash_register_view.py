from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from ..models.cash_register_model import CashRegister
from storeos.decorators import role_required


@role_required('Admin', 'Listar_Caja')
def cash_register_list_view(request):
    user_profile = request.user.userprofile
    company = user_profile.company

    cash_registers = CashRegister.objects.filter(
        company=company
    ).order_by('-created_at')

    selected_user = request.GET.get('user', '').strip()

    if selected_user:
        cash_registers = cash_registers.filter(user_id=selected_user)

    entries_per_page = request.GET.get('entries', 10)
    try:
        entries_per_page = int(entries_per_page)
    except ValueError:
        entries_per_page = 10

    entries_per_page = max(1, min(entries_per_page, 100))

    paginator = Paginator(cash_registers, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    users = get_user_model().objects.filter(
        userprofile__company=company
    ).order_by('username')

    context = {
        'page_obj': page_obj,
        'entries_per_page': entries_per_page,
        'users': users,
        'selected_user': selected_user,
    }

    return render(request, 'cash_register/list_cash_register.html', context)