from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ...models import Category
from storeos.decorators import role_required

@role_required('Admin', 'Cajero', 'Detalle_Categoria')
def category_detail(request, pk):
    """
    Display details of a category including its related items filtered by user's company.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the category to retrieve.

    Returns:
        HttpResponse: Rendered template with category details and related items.

    Raises:
        Http404: If the category does not exist or does not belong to user's company.
    """
    user_profile = request.user.userprofile  # Get user profile
    # Retrieve category filtered by user's company or return 404
    category = get_object_or_404(Category, pk=pk, company=user_profile.company)
    items = category.items.all()  # Related items via ManyToManyField's related_name 'items'

    return render(request, 'category/category_detail.html', {'category': category, 'items': items})
