from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from ...models import WikiCategory

@login_required
def wiki_category_list(request):
    """
    Paginated list of wiki categories for superusers.

    GET parameters:
    - entries: Number of categories per page (default: 10)
    - page: Page number (default: 1)

    Returns:
        Renders the template with the page object and entries count.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    categories = WikiCategory.objects.all()
    
    try:
        entries_per_page = max(1, int(request.GET.get('entries', 10)))
    except ValueError:
        entries_per_page = 10
    
    paginator = Paginator(categories, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'wiki_category/wiki_category_list.html', {
        'page_obj': page_obj,
        'entries_per_page': entries_per_page,
    })
