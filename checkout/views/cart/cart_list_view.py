from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from ...models import Cart
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Listar_Carro')
@login_required
def cart_list(request):
    """
    List carts filtered by search query and date for the user's company.

    Args:
        request (HttpRequest): The HTTP request object containing GET params:
            - search (str, optional): Text to search in username or payment method name.
            - date (str, optional): Date string in 'YYYY-MM-DD' format to filter carts by creation date.

    Returns:
        HttpResponse: Rendered template with filtered carts and pagination context.

    Raises:
        None
    """
    # Text search query from GET parameters
    search_query = request.GET.get('search', '')

    # Date filter query from GET parameters
    date_query = request.GET.get('date', '')

    # Filter carts belonging to the user's company
    filters = Q(company=request.user.userprofile.company)

    if search_query:
        # Filter by username or payment method name (case insensitive)
        filters &= Q(user__username__icontains=search_query) | Q(payment_method__name__icontains=search_query)

    if date_query:
        try:
            # Parse the date string and filter carts created on that date
            date_obj = datetime.strptime(date_query, '%Y-%m-%d')
            filters &= Q(created_at__date=date_obj.date())
        except ValueError:
            # Ignore invalid date format and do not apply date filter
            pass

    # Apply filters and order by newest carts first
    carts = Cart.objects.filter(filters).order_by('-created_at')

    # Render the template with carts and search parameters
    return render(request, 'checkout/cart_list.html', {
        'carts': carts,
        'page_obj': carts,
        'search_query': search_query,
        'date_query': date_query,
    })
