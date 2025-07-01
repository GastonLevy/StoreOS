from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from ...models import Category
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Listar_Categoria')
def category_list(request):
    """
    List categories filtered by the user's company with optional search and pagination.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered page with paginated categories and search context.

    Raises:
        None
    """
    user_profile = request.user.userprofile

    # Get search query from URL parameters
    search_query = request.GET.get('search', '')

    # Filter categories by the user's company
    categories = Category.objects.filter(company=user_profile.company)

    # Filter categories by name if search query exists
    if search_query:
        categories = categories.filter(name__icontains=search_query)

    # Pagination setup: entries per page (default 10)
    try:
        entries_per_page = int(request.GET.get('entries', 10))
    except ValueError:
        entries_per_page = 10

    # Limit entries per page to prevent abuse
    if entries_per_page < 1:
        entries_per_page = 10
    elif entries_per_page > 100:
        entries_per_page = 100

    paginator = Paginator(categories, entries_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'category/category_list.html',
        {
            'page_obj': page_obj,
            'entries_per_page': entries_per_page,
            'search_query': search_query  # Pass search term to template
        }
    )
