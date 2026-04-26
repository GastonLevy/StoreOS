from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from ...models import Person
from storeos.decorators import role_required


@role_required('Admin', 'Cajero', 'Listar_Usuario')
def account_list(request):
    """
    List Person accounts filtered by company and optional search query, with pagination.
    """
    user_profile = request.user.userprofile
    accounts = Person.objects.filter(company=user_profile.company)

    search_query = request.GET.get('search', '').strip()
    if search_query:
        accounts = accounts.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(dni__icontains=search_query)
        )

    entries_per_page = request.GET.get('entries', 10)
    try:
        entries_per_page = int(entries_per_page)
    except ValueError:
        entries_per_page = 10

    entries_per_page = max(1, min(entries_per_page, 100))

    paginator = Paginator(accounts, entries_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/account_list.html', {
        'page_obj': page_obj,
        'entries_per_page': entries_per_page,
        'search_query': search_query,
    })