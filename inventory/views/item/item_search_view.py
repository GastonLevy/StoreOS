from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ...models import Item
from django.db.models import Q
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Buscar_Producto')
def item_search(request):
    """
    Search for items by name or barcode within the user's company, excluding hidden items.

    Args:
        request (HttpRequest): The HTTP request containing the search query as GET parameter 'q'.

    Returns:
        JsonResponse: A list of matched items limited to 10, each with id, name, barcode, and price.

    Raises:
        None
    """
    query = request.GET.get('q', '')  # Get the user search query
    results = []

    if query:
        user_company = request.user.userprofile.company  # Get user's company

        # Search items by name or barcode, filter by company and exclude hidden items
        items = Item.objects.filter(
            Q(name__icontains=query) | Q(barcode__icontains=query),
            company=user_company,
            hide=False
        )[:10]  # Limit to 10 results

        # Prepare data for JSON response
        results = [
            {
                'id': item.id,
                'name': item.name,
                'barcode': item.barcode,
                'price': float(item.price),
            } for item in items
        ]

    return JsonResponse(results, safe=False)
