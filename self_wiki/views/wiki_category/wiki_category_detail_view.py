from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ...models import WikiCategory

@login_required
def wiki_category_detail(request, pk):
    """
    Displays the details of a specific wiki category.
    
    Accessible only to superusers.

    Args:
        request: HttpRequest object.
        pk: Category ID.

    Returns:
        Renders the template with the category or 404 error if not found.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    category = get_object_or_404(WikiCategory, pk=pk)
    
    return render(request, 'wiki_category/wiki_category_detail.html', {'category': category})
